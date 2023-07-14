from django.urls import path, include
from . import views

app_name = "base"
urlpatterns = [
    path("", views.index, name='index'),
    path("rooms/", views.rooms, name="rooms"),
    path("room/<int:pk>/", views.room, name="room"),
]
