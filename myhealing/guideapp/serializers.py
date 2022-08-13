from rest_framework import serializers
from .models import *
from accounts.serializers import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('sort', 'title')

class GuideImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideImage
        fields = ('id', 'image', 'guide', 'thumbnail')
        guide = serializers.Field(source='guide.id')

class GuideSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    images = GuideImageSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Guide
        fields = (
            'id', 
            'user',
            'date', 
            'created_at', 
            'updated_at', 
            'place',
            'cost', 
            'title', 
            'body', 
            'address', 
            'views', 
            'tag',
            'images'
        )
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        del rep["user"]
        return rep

class GuideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ('id', 'user', 'created_at', 'title', 'summary')

class RandomGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = RandomGuide
        fields = "__all__"