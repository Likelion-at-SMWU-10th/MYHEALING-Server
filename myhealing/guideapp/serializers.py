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
            'star',
            'tag',
            'images',
            'love_count'
        )
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        del rep["user"]
        return rep

class GuideListSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(method_name='get_user_name')
    user_profile_image = serializers.SerializerMethodField(method_name='get_user_profile')
    class Meta:
        model = Guide
        fields = ('id', 'user_name', 'user_profile_image', 'created_at', 'title', 'summary')
    
    def get_user_name(self, obj):
        return obj.user.nickname
    
    def get_user_profile(self, obj):
        return obj.user.profile_photo.url

class RandomGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = RandomGuide
        fields = "__all__"