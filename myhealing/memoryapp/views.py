from django.http import Http404
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *

import os

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
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

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

    # /memory/<int:memory_id>
    def put(self, request, memory_id):
        # TODO: 1) 기본 내용(title, body, place, scope, thumbnail) 수정
        memory = self.get_object(memory_id)
        file_change_check = request.POST.get('file_change', False)
        serializer = MemorySerializer(memory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # TODO: 2) 사진 변경이 있는 경우 이미지는 전체 삭제 후 다시 저장
            # *사진 변경이 있는 경우 - 1. 기존 사진이 없다가 생기는 경우, 2. 사진의 개수 혹은 다른 사진으로 변경, 3. 사진 삭제
            # 2-1) 전체 삭제
            if file_change_check:
                images = MemoryImage.objects.filter(memory=memory.id)
                if images: # 기존 사진이 없는 경우 delete 진행 X
                    for image in images:
                        image.delete()
                    os.remove(os.path.join(settings.MEDIA_ROOT, 'img/memory', str(memory_id)).replace('\\','/'))
            # 2-2) 다시 저장
            images_data = request.FILES.getlist('image')
            for image_data in images_data:
                MemoryImage.objects.create(memory=memory, image=image_data)
            return Response(data=serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class MemoryImageList(APIView):
    # /memory/images/<int:memory_id>
    def get(self, request, memory_id, format=None):
        images = MemoryImage.objects.filter(memory=memory_id)
        serializer_context = {'request':request,}
        serializer = MemoryImageSerializer(images, context=serializer_context, many=True)
        return Response(data=serializer.data, status = status.HTTP_200_OK)
