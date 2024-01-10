from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from accounts.models import UserProfile
from .utils import generate_room_code


def index(request):
    user_profiles = UserProfile.objects.all().exclude(user__username=request.user.username)
    user_rooms = {}

    for profile in user_profiles:
        user_pair = tuple(sorted([request.user.username, profile.user.username]))
        room_name = generate_room_code(user_pair[0], user_pair[1])
        user_rooms[profile.user.username] = room_name
        print(user_rooms[profile.user.username])

        print(room_name)

    context = {
        'user_profiles': user_profiles,
        'user_rooms': user_rooms,
    }
    return render(request, "chat/index.html", context)




@login_required(login_url='login')
def room(request, room_name):
    messages = Message.objects.filter(room_name=room_name).order_by('-time_stamp').all()[:20]

    context = {
        "room_name": room_name,
        'username': mark_safe(json.dumps(request.user.username)),
        'chats': messages[::-1],  
    }
    return render(request, "chat/room.html", context)


