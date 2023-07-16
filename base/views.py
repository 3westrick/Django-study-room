from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from .models import Room, Topic, RoomMessage, User
from .forms import RoomForm, UserForm,MyUserCreationForm
from django.db.models import Q


# Create your views here.
def topicsPage(request):
    search = request.GET.get('search', '')
    if search:
        topics = Topic.objects.filter(
            Q(name__icontains=search)
        )
    else:
        topics = Topic.objects.all()
    return render(request, 'base/topics.html', {'topics': topics})


def activotyPage(request):
    room_messages = RoomMessage.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})


@login_required
def edit_profile(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("base:profile", user.id)
    return render(request, 'base/edit_profile.html', {
        'user': user,
        'form': form,
    })


@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    rooms_list = user.room_set.all()
    room_messages = user.roommessage_set.all()
    topics = Topic.objects.all()[:5]
    return render(request, 'base/profile.html', {
        'user': user,
        'rooms': rooms_list,
        'room_messages': room_messages,
        'topics': topics
    })


def signin(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('base:index')
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("base:index")
        else:
            messages.error(request, "Username or Password does not exist.")

    return render(request, 'base/auth.html', {'page': page})


@login_required
def signout(request):
    logout(request)
    return redirect("base:index")


def signup(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("base:index")
        else:
            messages.error(request, "An error occurred during registration")
    return render(request, 'base/auth.html', {'form': form})


def index(request):
    return redirect("base:rooms")


def rooms(request):
    search = request.GET.get('search', '')
    if search:
        # i in icontains means "not case sensitive"
        room_list = Room.objects.filter(
            Q(topic__name__icontains=search) |
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    else:
        room_list = Room.objects.all()
    topics = Topic.objects.all()[:5]
    room_messages = RoomMessage.objects.filter(Q(room__name__icontains=search) | Q(room__topic__name__icontains=search))
    return render(request, 'base/new_rooms.html', {
        'rooms': room_list,
        'topics': topics,
        'search': search,
        'room_messages': room_messages,
    })


def room(request, pk):
    room_item = get_object_or_404(Room, pk=pk)
    room_messages = room_item.roommessage_set.all()  # one to many use lowercase and _set
    members = room_item.members.all()  # u can use filter here too
    if request.method == 'POST':
        message = RoomMessage.objects.create(
            user=request.user,
            room=room_item,
            text=request.POST.get('text')
        )
        return redirect('base:room', pk=room_item.id)
    room_item.members.add(request.user)
    return render(request, 'base/room.html', {'room': room_item, 'room_messages': room_messages, 'members': members})


@login_required
def create(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic)
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room_item = form.save(commit=False)
        #     room_item.host = request.user
        #     room_item.save()
        #     return redirect('base:index')
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect("base:rooms")
    return render(request, 'base/room_form.html', {'form': form, 'title': 'Create', 'topics': topics})


@login_required
def edit(request, pk):
    room_item = get_object_or_404(Room, pk=pk)
    form = RoomForm(instance=room_item)
    topics = Topic.objects.all()

    if request.user != room_item.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        # form = RoomForm(request.POST, instance=room_item)
        # if form.is_valid():
        #     form.save()
        #     return redirect('base:index')
        topic = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic)
        room_item.name = request.POST.get('name')
        room_item.description = request.POST.get('description')
        room_item.topic = topic
        return redirect('base:index')
    return render(request, 'base/room_form.html', {
        'form': form,
        'title': 'Update',
        'room': room_item,
        'topics': topics,
    })


@login_required
def delete_room(request, pk):
    room_item = get_object_or_404(Room, pk=pk)
    if request.user != room_item.host:
        return HttpResponse("You are not allowed here!!")
    if request.method == 'POST':
        room_item.delete()
        return redirect('base:index')
    return render(request, 'base/delete.html', {'obj': room_item})


@login_required
def delete_msg(request, pk):
    msg = get_object_or_404(RoomMessage, pk=pk)
    if request.user != msg.user:
        return HttpResponse("You are not allowed here!!")
    if request.method == 'POST':
        msg.delete()
        return redirect('base:index')
    return render(request, 'base/delete.html', {'obj': msg})
