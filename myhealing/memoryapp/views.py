from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *

class MemoryList(APIView):
    # /memory
    def get(self, request):
        # TODO: user_id filter 추후 추가 필요
        memories = Memory.objects.all()
        serializer = MemoryListSerializer(memories, many=True)
        return Response(serializer.data)
    
    # /memory
    def post(self, request, *args, **kwargs):
        images_data = request.FILES.getlist('image')
        serializer = MemorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            memory = get_object_or_404(Memory, pk=serializer.data['id'])
            for image_data in images_data:
                MemoryImage.objects.create(memory=memory, image=image_data)
            return Response(data=serializer.data)
        return Response(serializer.error, status.HTTP_400_BAD_REQUEST)

class MemoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Memory.objects.get(pk=pk)
        except Memory.DoesNotExist:
            raise Http404

    # /memory/<int:memory_id>
    def get(self, request, memory_id):
        memory = self.get_object(memory_id)
        serializer = MemorySerializer(memory)
        return Response(serializer.data)

class MemoryImageList(APIView):
    # /memory/images/<int:memory_id>
    def get(self, request, memory_id, format=None):
        images = MemoryImage.objects.filter(memory=memory_id)
        serializer_context = {'request':request,}
        serializer = MemoryImageSerializer(images, context=serializer_context, many=True)
        return Response(data=serializer.data, status = status.HTTP_200_OK)
