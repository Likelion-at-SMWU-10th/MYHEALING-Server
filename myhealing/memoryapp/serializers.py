from rest_framework import serializers
from .models import *

class MemoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemoryImage
        fields = ('id', 'image', 'memory')
        memory = serializers.Field(source='memory.id')

class MemorySerializer(serializers.ModelSerializer):
    images = MemoryImageSerializer(many=True, read_only=True)
    class Meta:
        model = Memory
        fields = ('id', 'updated_at', 'date', 'place', 'title', 'body', 'scope', 'thumbnail', 'images')

class MemoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ('id', 'updated_at', 'title')
