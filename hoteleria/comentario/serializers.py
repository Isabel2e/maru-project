from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Word


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_staff', 'date_joined']
        read_only_fields = ['is_staff', 'date_joined']

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'word', 'language', 'created_at']