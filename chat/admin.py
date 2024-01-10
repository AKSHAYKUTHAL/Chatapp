from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ['author','content','time_stamp','room_name']

admin.site.register(Message,MessageAdmin)