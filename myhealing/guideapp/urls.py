from django.db import router
from django.urls import path
from .views import *

from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', GuideList.as_view()),
    path('<int:pk>', GuideDetail.as_view()),
    path('search/', GuideSearch.as_view()),
    path('recommend/', GuideRecommend.as_view()),
    path('tags/', TagList.as_view()),
    path('highviews/', GuideHighView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)