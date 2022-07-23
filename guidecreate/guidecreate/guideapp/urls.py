from django.urls import path
from .views import GuideList, GuideDetail

urlpatterns = [
    path('guide/', GuideList.as_view()),
    path('guide/<int:pk>', GuideDetail.as_view()),
]