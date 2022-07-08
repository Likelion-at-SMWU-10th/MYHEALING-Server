from django.contrib import admin
from django.urls import path, include
from myhealingapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('accounts/', include('accounts.urls')),
]
