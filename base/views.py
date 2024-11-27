from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, CustomCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import User
from django.utils.text import slugify


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
     
        # checks if user exist
        try:
            user = User.objects.get(email=email)
             # make sure credentials of the user are correct in case it exist and return it
            user = authenticate(request, email=email, password=password)
            
            # if user is returned
            if user is not None:
                # adding session to db and browser(logged in)
                login(request, user) 
                return redirect('home')
            else:
                messages.error(request, 'Username or Password does not exist')

        except:
            messages.error(request, "User does not exist")
            
     
    context = {'page': page}
    return render(request, 'base/login_signup.html', context)

def logoutUser(request):

    logout(request)
    return redirect('home')
def signupPage(request):
    form = CustomCreationForm()

    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            if not user.slug:  # Ensure slug is generated if not present
                user.slug = slugify(user.username)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            # This will show a general error message on form level
            messages.error(request, 'Error: Please validate your input')

    context = {'form': form}
    return render(request, 'base/login_signup.html', context)

# Function-based-views
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) | 
        Q(description__icontains=q)
        )
    # rooms = Room.objects.all()

    topics = Topic.objects.all()
    room_count = rooms.count()
    msgs = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )


    roomsContext = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'msgs':msgs}
    return render(request, 'base/home.html', roomsContext)

def profile(request, slug):
    user = User.objects.get(slug=slug)
    rooms = user.room_set.all()
    msgs = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms':rooms, 'msgs':msgs, 'topics':topics}

    return render(request, 'base/profile.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    msgs = room.message_set.all().order_by('created')
    participants = room.participants.all()
    if(request.method == 'POST'):
        msg = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    print(participants)
    context = {'room':room, 'msgs':msgs, 'participants':participants}
    print(context)
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == 'POST':

        # search for a topic, if exists return obj if not create it

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        # create room obj
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

        #print(request.POST)
    context={'form' : form, 'topics':topics}

    return render(request, 'base/room_form.html', context) 

@login_required(login_url='login')
def updateRoom(request, pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # render empty form and put instace (form details) in it

    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic # in case user created new topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context={'form' : form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to delete this room')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room': room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'msg': message}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            # Ensure that the slug is set after updating the profile
            if not user.slug:
                user.slug = slugify(user.username)

            return redirect('profile', slug=user.slug)  # Redirect to the profile with the slug

    context = {'form': form}
    return render(request, 'base/updateProfile.html', context)

def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics':topics}
    return render(request, 'base/topicsPage.html', context)

def discussions(request):
    msgs = Message.objects.all()[:3]  # Limit to the latest 3 msgs
    context = {'msgs': msgs}
    return render(request, 'base/discussionPage.html', context)
