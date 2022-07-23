from django.urls import path
from .views import GuideList

urlpatterns = [
    path('guide/', GuideList.as_view()),
]