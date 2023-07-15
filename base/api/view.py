from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Room, Topic, RoomMessage
from .serializers import RoomSerializer


@api_view(['GET'])
def get_routes(request):
    routs = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routs)


@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_room(request, pk):
    room = Room.objects.get(pk=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
