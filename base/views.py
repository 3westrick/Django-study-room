from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from .models import Room


# Create your views here.
def index(request):
    return render(request, 'base/index.html')


def rooms(request):
    room_list = get_list_or_404(Room)
    return render(request, 'base/rooms.html', {'rooms': room_list})


def room(request, pk):
    room_item = get_object_or_404(Room, pk=pk)
    return render(request, 'base/room.html', {'room': room_item})
