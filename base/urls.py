from django.urls import path, include
from . import views

app_name = "base"
urlpatterns = [
    path("", views.index, name='index'),
    path("rooms/", views.rooms, name="rooms"),
    path("room/<int:pk>/", views.room, name="room"),
    path("room/create/", views.create, name="create"),
    path("room/<int:pk>/edit/", views.edit, name="edit"),
    path("room/<int:pk>/delete/", views.delete, name="delete"),
]
