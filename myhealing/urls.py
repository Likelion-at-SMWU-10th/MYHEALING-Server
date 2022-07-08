from django.contrib import admin
from django.urls import path, include
import accounts.views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="login/index.html")),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]