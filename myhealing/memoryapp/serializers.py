from rest_framework import serializers
from .models import *
from accounts.serializers import UserSerializer

class MemoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryImage
        fields = ('id', 'image', 'memory', 'thumbnail')
        memory = serializers.Field(source='memory.id')

class MemorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = MemoryImageSerializer(many=True, read_only=True)
    class Meta:
        model = Memory
        fields = (
            'id', 
            'user',
            'created_at',
            'updated_at', 
            'date', 
            'place', 
            'title', 
            'body', 
            'scope', 
            'images'
        )
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        del rep["user"]
        return rep

class MemoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ('id', 'created_at', 'title')
