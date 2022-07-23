from rest_framework import serializers
from .models import Guide

class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ('id', 'title', 'date', 'buy', 'body')

class GuideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ('id', 'title', 'date', 'summary')