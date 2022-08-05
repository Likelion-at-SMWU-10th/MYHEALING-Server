from rest_framework import serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('sort', 'title')

class GuideSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    class Meta:
        model = Guide
        fields = ('id', 'creator_id', 'date', 'created_at', 'updated_at', 'place',
        'cost', 'title', 'body', 'address', 'views', 'thumbnail', 'tag')

class GuideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ('id', 'creator_id', 'created_at', 'title', 'summary')