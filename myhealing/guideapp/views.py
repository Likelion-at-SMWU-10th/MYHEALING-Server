import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.db.models import Count

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

class GuideDetail(APIView):
    def get_object(self, pk):
        try:
            return Guide.objects.get(pk=pk)
        except Guide.DoesNotExist:
            raise Http404

    def get(self, request, pk): # guide
        guide = self.get_object(pk)
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

class GuideSearch(APIView):
    def get(self, request):
        scope = request.GET.get('filter', '') # title, body, mix
        query = request.GET.get('query', '')
        if query:
            if scope == 'title': # 제목만
                guide_objects = Guide.objects.filter(title__icontains = query).order_by("-updated_at")
            elif scope == 'body': # 본문만
                guide_objects = Guide.objects.filter(body__icontains = query).order_by("-updated_at")
            else: # 제목 + 본문
                guide_objects = (Guide.objects.filter(title__icontains=query) | Guide.objects.filter(body__icontains=query)).order_by("-updated_at")
            
            # serializer = GuideListSerializer(guide_objects, many=True)
            serializer = GuideSerializer(guide_objects, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GuideRecommend(APIView):
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
        # serializer = GuideListSerializer(guides, many=True)
        serializer = GuideSerializer(guides, many=True)
        return Response(serializer.data)

        
