from django.urls import path
from . import view

urlpatterns = [
    path('', view.get_routes),
    path('rooms/', view.get_rooms),
    path('rooms/<int:pk>/', view.get_room),
]
