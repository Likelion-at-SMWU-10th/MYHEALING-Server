from django.urls import path
from memoryapp import views

urlpatterns = [
    path('', views.home, name='home'),
]