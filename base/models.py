from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
import uuid


class User(AbstractUser):
    slug = models.SlugField(primary_key=True,unique=True, blank=True, editable=False)
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=250, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null = True, default = "avatar.svg") 
  
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [

    ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# db table (room)
class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True) # everytime save method is called, django updates date-timefield
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add = True)


    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
    
