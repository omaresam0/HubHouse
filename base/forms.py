from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

class CustomCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username', 'email', 'password1','password2']
        error_messages = {
            'username': {
                'required': 'Please provide your username.',
                'unique': 'This username is already taken.',
            },
            'email': {
                'required': 'Email is required.',
                'invalid': 'Enter a valid email address.',
            },
            'password1': {
                'required': 'Please provide a password.',
            },
            'password2': {
                'required': 'Please confirm your password.',
                'password_mismatch': 'The two passwords do not match.',
            },
        }
class RoomForm(ModelForm):
    class Meta:    
        model = Room # create form for room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta: 
        model = User
        fields = ['avatar','name','username', 'email', 'bio']
