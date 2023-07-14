from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm


# Create your views here.
def index(request):
    return render(request, 'base/index.html')


def rooms(request):
    room_list = get_list_or_404(Room)
    return render(request, 'base/rooms.html', {'rooms': room_list})


def room(request, pk):
    room_item = get_object_or_404(Room, pk=pk)
    return render(request, 'base/room.html', {'room': room_item})


def create(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base:index')
    return render(request, 'base/room_form.html', {'form': form})


def edit(request, pk):
    room_item = get_object_or_404(Room, pk=pk)
    form = RoomForm(instance=room_item)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room_item)
        if form.is_valid():
            form.save()
            return redirect('base:index')

    return render(request, 'base/room_form.html', {'form': form})


def delete(request, pk):
    room_item = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room_item.delete()
        return redirect('base:index')
    return render(request, 'base/delete.html', {'obj': room_item})
