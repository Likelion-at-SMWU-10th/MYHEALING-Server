from django.http import Http404
from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *
from .pagination import PaginationHandlerMixin

import os
import shutil

class MemoPagination(PageNumberPagination):
    page_size_query_param = 'limit'

class MypageMemoryList(APIView):
    def get(self, request):
        memories = Memory.objects.filter(user=request.user).order_by("-created_at")

        serializer = MemoryListSerializer(memories, many=True)
        return Response(serializer.data)


class MemoryList(APIView, PaginationHandlerMixin):
    pagination_class = MemoPagination
    serializer_class = MemoryListSerializer

    # /memory
    def get(self, request):
        memories = Memory.objects.all().order_by("-created_at")

        page = self.paginate_queryset(memories)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(memories, many=True)
        return Response(serializer.data)
    
    # /memory
    def post(self, request, *args, **kwargs):
        images_data = request.FILES.getlist('image')
        serializer = MemorySerializer(data=request.data)
        if serializer.is_valid():
            memory = serializer.save(user=request.user)
            for i in range(len(images_data)):
                if i==0:
                    MemoryImage.objects.create(memory=memory, image=images_data[i], thumbnail=True)
                else:
                    MemoryImage.objects.create(memory=memory, image=images_data[i])
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
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
        sdc = serializer.data.copy()
        if memory.user == request.user:
            sdc['is_writer'] = True
        else:
            sdc['is_writer'] = False

        return Response(sdc)

    # /memory/<int:memory_id>
    def put(self, request, memory_id):
        # 1) 기본 내용(title, body, place, scope, thumbnail) 수정
        memory = self.get_object(memory_id)
        file_change_check = request.POST.get('file_change', False)
        serializer = MemorySerializer(memory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 2) 사진 변경이 있는 경우 이미지는 전체 삭제 후 다시 저장
            # *사진 변경이 있는 경우 - 1. 기존 사진이 없다가 생기는 경우, 2. 사진의 개수 혹은 다른 사진으로 변경, 3. 사진 삭제
            # 2-1) 전체 삭제
            if file_change_check:
                images = MemoryImage.objects.filter(memory=memory.id)
                if images: # 기존 사진이 없는 경우 delete 진행 X
                    for image in images:
                        image.delete()
                    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'img/memory', str(memory_id)).replace('\\','/'), ignore_errors=True)
                # 2-2) 다시 저장
                images_data = request.FILES.getlist('image')
                for image_data in images_data:
                    MemoryImage.objects.create(memory=memory, image=image_data)
            return Response(data=serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    # /memory/<int:memory_id>
    def delete(self, request, memory_id):
        memory = self.get_object(memory_id)
        memory.delete()
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'img/memory', str(memory_id)).replace('\\','/'), ignore_errors=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MemoryImageList(APIView):
    # /memory/images/<int:memory_id>
    def get(self, request, memory_id, format=None):
        images = MemoryImage.objects.filter(memory=memory_id)
        serializer_context = {'request':request,}
        serializer = MemoryImageSerializer(images, context=serializer_context, many=True)
        return Response(data=serializer.data, status = status.HTTP_200_OK)
