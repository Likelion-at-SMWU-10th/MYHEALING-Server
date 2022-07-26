from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name="myhealingapp/index.html")),
    path('admin/', admin.site.urls),
    path('memory/', include('memoryapp.urls')),
    path('guide/', include('guideapp.urls')),
]

urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
