from django.shortcuts import render
from django.http import HttpResponse

rooms_ = [
    {
        'name': 'Python',
        'id': 1,
    },
    {
        'name': 'Django',
        'id': 2,
    },
    {
        'name': 'Java',
        'id': 3,
    },
]


# Create your views here.
def index(request):
    return render(request, 'base/index.html')


def rooms(request):
    return render(request, 'base/rooms.html', {'rooms': rooms_})


def room(request, pk):
    temp = None
    for room_ in rooms_:
        if room_['id'] == pk:
            temp = room_
    return render(request, 'base/room.html', {'room': temp})
