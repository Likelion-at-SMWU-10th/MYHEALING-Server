from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

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