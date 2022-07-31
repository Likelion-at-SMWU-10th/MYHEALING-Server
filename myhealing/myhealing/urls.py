from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('memory/', include('memoryapp.urls')),
    path('guide/', include('guideapp.urls')),
    path('kakao/', include('accounts.urls')),
]

urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
