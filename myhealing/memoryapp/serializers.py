from rest_framework import serializers
from .models import *

class MemoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryImage
        fields = ('id', 'image', 'memory', 'thumbnail')
        memory = serializers.Field(source='memory.id')

class MemorySerializer(serializers.ModelSerializer):
    images = MemoryImageSerializer(many=True, read_only=True)
    class Meta:
        model = Memory
        fields = (
            'id', 
            'created_at',
            'updated_at', 
            'date', 
            'place', 
            'title', 
            'body', 
            'scope', 
            'images'
        )

class MemoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ('id', 'created_at', 'title')
