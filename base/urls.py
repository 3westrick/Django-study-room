from django.urls import path, include
from . import views

app_name = "base"
urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.signin, name='login'),
    path("logout/", views.signout, name='logout'),
    path("signup/", views.signup, name='reg'),
    path("rooms/", views.rooms, name="rooms"),
    path("room/<int:pk>/", views.room, name="room"),
    path("room/create/", views.create, name="create"),
    path("room/<int:pk>/edit/", views.edit, name="edit"),
    path("room/<int:pk>/delete-room/", views.delete_room, name="delete-room"),
    path("room/<int:pk>/delete-msg/", views.delete_msg, name="delete-msg"),
]
