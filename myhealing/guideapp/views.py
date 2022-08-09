import json
import random
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Max
from django.http import Http404

from .serializers import GuideSerializer, GuideListSerializer, RandomGuideSerializer, TagSerializer
from .models import Guide, RandomGuide, Tag
from .pagination import PaginationHandlerMixin

# Create your views here.
class MemoPagination(PageNumberPagination):
    page_size_query_param = 'limit'

class TagList(APIView):
    def get(self, request):
        tags = Tag.objects.all().order_by("sort")
        serializer = TagSerializer(tags, many=True)
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
        tags = request.data.get('tag')
        if serializer.is_valid():
            guide = serializer.save()
            if tags:
                for tag in tags:
                    try: 
                        guide.tag.add(Tag.objects.get(title=tag))
                    except Tag.DoesNotExist:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
        return Response(serializer.data)

    def put(self, request, pk):
        guide = self.get_object(pk)
        serializer = GuideSerializer(guide, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guide = self.get_object(pk)
        guide.delete()
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

