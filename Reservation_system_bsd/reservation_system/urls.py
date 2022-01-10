"""reservation_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reservation_app.views import add_room, modify_room, delete_room, room_reservation, room_details, \
    rooms_list

urlpatterns = [
    path('admin/', admin.site.urls),

    path('room/new/', add_room),
    path('room/modify/<int:room_id>', modify_room),
    path('room/delete/<int:room_id>', delete_room),
    path('room/reserve/<int:room_id>', room_reservation),
    path('room/<int:room_id>', room_details),
    path('rooms/', rooms_list),
]
