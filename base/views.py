from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Room, Topic, RoomMessage
from .forms import RoomForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q


# Create your views here.

def signin(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('base:index')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
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
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
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
    return render(request, 'base/index.html')


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
    topics = get_list_or_404(Topic)
    return render(request, 'base/rooms.html', {
        'rooms': room_list,
        'topics': topics,
        'search': search,
    })


def room(request, pk):
    room_item = get_object_or_404(Room, pk=pk)
    return render(request, 'base/room.html', {'room': room_item})


@login_required
def create(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base:index')
    return render(request, 'base/room_form.html', {'form': form})


@login_required
def edit(request, pk):
    room_item = get_object_or_404(Room, pk=pk)
    form = RoomForm(instance=room_item)

    if request.user != room_item.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room_item)
        if form.is_valid():
            form.save()
            return redirect('base:index')

    return render(request, 'base/room_form.html', {'form': form})


@login_required
def delete(request, pk):
    room_item = get_object_or_404(Room, pk=pk)
    if request.user != room_item.host:
        return HttpResponse("You are not allowed here!!")
    if request.method == 'POST':
        room_item.delete()
        return redirect('base:index')
    return render(request, 'base/delete.html', {'obj': room_item})
