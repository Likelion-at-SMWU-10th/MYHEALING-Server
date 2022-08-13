from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', MemoryList.as_view()),
    path('<int:memory_id>', MemoryDetail.as_view()),
    path('images/<int:memory_id>', MemoryImageList.as_view()),
    path('mypage/', MypageMemoryList.as_view()),
]