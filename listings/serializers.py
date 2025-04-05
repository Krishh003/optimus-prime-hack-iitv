from rest_framework import serializers
from .models import ChatMessage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'receiver_id', 'message', 'created_at', 'is_read']
        read_only_fields = ['sender', 'created_at', 'is_read'] 