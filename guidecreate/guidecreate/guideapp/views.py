from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import GuideSerializer, GuideListSerializer
from .models import Guide

# Create your views here.
class GuideList(APIView):
    def get(self, request):
        guides = Guide.objects.all()

        serializer = GuideListSerializer(guides, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)