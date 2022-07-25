from django.db import router
from django.urls import path
from .views import GuideList, GuideDetail

from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('guide/', GuideList.as_view()),
    path('guide/<int:pk>', GuideDetail.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)