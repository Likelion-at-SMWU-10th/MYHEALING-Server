import json
import random
import shutil
import os
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Max
from django.http import Http404
from django.conf import settings
from django.shortcuts import get_object_or_404

from .serializers import GuideSerializer, GuideListSerializer, RandomGuideSerializer, TagSerializer
from .models import Guide, RandomGuide, Tag, GuideImage, Love
from .pagination import PaginationHandlerMixin

# Create your views here.
class MemoPagination(PageNumberPagination):
    page_size_query_param = 'limit'

class TagList(APIView):
    def get(self, request):
        tags = Tag.objects.all().order_by("sort")
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

class MypageGuideList(APIView, PaginationHandlerMixin):
    pagination_class = MemoPagination
    serializer_class = GuideListSerializer

    def get(self, request):
        guides = Guide.objects.filter(user=request.user).order_by("-created_at")

        page = self.paginate_queryset(guides)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(page, many=True)
        return Response(serializer.data)


class GuideList(APIView, PaginationHandlerMixin):
    pagination_class = MemoPagination
    serializer_class = GuideListSerializer

    def get(self, request):
        guides = Guide.objects.all()

        page = self.paginate_queryset(guides)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(guides, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuideSerializer(data=request.data)
        tag_input = request.data.get('tag')
        if tag_input:
            tags = json.loads(tag_input)
        else:
            tags = None
        
        images = request.FILES.getlist('image')
        if serializer.is_valid():
            guide = serializer.save(user=request.user)

            # 태그 추가
            if tags:
                for tag in tags:
                    try: 
                        guide.tag.add(Tag.objects.get(title=tag))
                    except Tag.DoesNotExist:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # 이미지 추가
            for i in range(len(images)):
                if i==0:
                    GuideImage.objects.create(guide=guide, image=images[i], thumbnail=True)
                else:
                    GuideImage.objects.create(guide=guide, image=images[i])
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GuideDetail(APIView):
    def get_object(self, pk):
        try:
            return Guide.objects.get(pk=pk)
        except Guide.DoesNotExist:
            raise Http404

    def get(self, request, pk): # guide
        guide = self.get_object(pk)
        # 조회 수 증가
        guide.views += 1
        guide.save()

        serializer = GuideSerializer(guide)
        sdc = serializer.data.copy()
        if guide.user == request.user:
            sdc['is_writer'] = True
        else:
            sdc['is_writer'] = False

        return Response(sdc)

    def put(self, request, pk):
        guide = self.get_object(pk)
        tag_input = request.POST.get('tag')
        if tag_input:
            tags = json.loads(tag_input)
        else:
            tags = None
        file_change_check = request.POST.get('file_change', False)
        serializer = GuideSerializer(guide, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 태그 수정
            # 1) 태그 전체 삭제
            guide.tag.clear()
            # 2) 태그 추가
            if tags:
                for tag in tags:
                    try: 
                        guide.tag.add(Tag.objects.get(title=tag))
                    except Tag.DoesNotExist:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # 사진 변경이 있는 경우
            if file_change_check:
                images = GuideImage.objects.filter(guide=guide.id)
                if images: # 기존 사진이 없는 경우 delete 진행 X
                    for image in images:
                        image.delete()
                    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'img/guide', str(pk)).replace('\\', '/'), ignore_errors=True)
            # 다시 저장
            images_data = request.FILES.getlist('image')
            for i in range(len(images_data)):
                if i==0:
                    GuideImage.objects.create(guide=guide, image=images_data[i], thumbnail=True)
                else:
                    GuideImage.objects.create(guide=guide, image=images_data[i])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guide = self.get_object(pk)
        guide.delete()
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'img/guide', str(pk)).replace('\\', '/'), ignore_errors=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

class GuideSearch(APIView, PaginationHandlerMixin):
    pagination_class = MemoPagination
    serializer_class = GuideListSerializer

    def get(self, request):
        scope = request.GET.get('filter', '') # title, body, mix
        query = request.GET.get('query', '')
        if query:
            if scope == 'title': # 제목만
                guide_objects = Guide.objects.filter(title__icontains = query).order_by("-created_at")
            elif scope == 'body': # 본문만
                guide_objects = Guide.objects.filter(body__icontains = query).order_by("-created_at")
            else: # 제목 + 본문
                guide_objects = (Guide.objects.filter(title__icontains=query) | Guide.objects.filter(body__icontains=query)).order_by("-created_at")
            
            page = self.paginate_queryset(guide_objects)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
            else:
                serializer = self.serializer_class(guide_objects, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GuideRecommend(APIView, PaginationHandlerMixin):
    pagination_class = MemoPagination
    serializer_class = GuideListSerializer

    def get(self, request):
        keywords = json.loads(request.GET.get('keyword', ''))
        region = request.GET.get('region', '')
        # keyword는 하나 이상 선택하도록, region은 없을 경우 전체 검색
        if not keywords:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not region:
            guides = Guide.objects.all()
        else:
            guides = Guide.objects.filter(address__icontains = region)

        for keyword in keywords:
            guides = guides.filter(tag__title=keyword)
        
        page = self.paginate_queryset(guides)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(guides, many=True)
        return Response(serializer.data)

class GuideHighView(APIView):
    def get(self, request):
        guides = Guide.objects.order_by("-views")[:3]
        serializer = GuideSerializer(guides, many=True)
        return Response(serializer.data)

class RandomGuideList(APIView):
    def get(self, request):
        random_guides = RandomGuide.objects.all()
        serializer = RandomGuideSerializer(random_guides, many=True)
        return Response(serializer.data)

class RandomGuideOne(APIView):
    def get(self, request):
        max_id = RandomGuide.objects.all().aggregate(max_id=Max("id"))['max_id']
        while True:
            pk = random.randint(1, max_id)
            random_guide = RandomGuide.objects.filter(pk=pk).first()
            if random_guide:
                serializer = RandomGuideSerializer(random_guide)
                return Response(serializer.data)

class GuideLove(APIView, PaginationHandlerMixin):
    pagination_class = MemoPagination
    serializer_class = GuideListSerializer
    
    def get(self, request):
        guides_loved_pk = Love.objects.filter(user=request.user).values_list('guide', flat=True).order_by("-created_at")
        guides = Guide.objects.filter(pk__in=guides_loved_pk)

        page = self.paginate_queryset(guides)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(page, many=True)
        return Response(serializer.data)

    def post(self, request, guide_id):
        current_user = request.user
        guide = Guide.objects.get(pk=guide_id)

        current_user_guides = Love.objects.filter(user=current_user)
        dup_guide_check = current_user_guides.filter(guide=guide)
        if dup_guide_check:
            return Response({
                "message": "already exists in guide_loved_set"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        Love.objects.create(guide=guide, user=current_user)

        return Response(status=status.HTTP_201_CREATED)
    
    def delete(self, request, guide_id):
        guide = get_object_or_404(Guide, pk=guide_id)
        love = Love.objects.filter(user=request.user).filter(guide=guide)
        if not love:
            return Response({
                "message": "DoesNotExist, you might not loved this guide before"
            }, status=status.HTTP_404_NOT_FOUND)
        
        love.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
