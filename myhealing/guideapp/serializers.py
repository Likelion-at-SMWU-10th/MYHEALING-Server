from rest_framework import serializers
from .models import Guide

class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ('id', 'creator_id', 'date', 'created_at', 'updated_at', 'place',
        'cost', 'title', 'body', 'address', 'views', 'thumbnail')

class GuideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ('id', 'creator_id', 'created_at', 'title', 'summary')