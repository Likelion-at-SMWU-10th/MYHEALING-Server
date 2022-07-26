from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', TemplateView.as_view(template_name="myhealingapp/index.html")),
    path('admin/', admin.site.urls),
    path('guide/', include('guideapp.urls')),
]