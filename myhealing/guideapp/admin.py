from django.contrib import admin
from .models import Guide, Tag, RandomGuide, GuideImage

# Register your models here.
admin.site.register(Guide)
admin.site.register(Tag)
admin.site.register(RandomGuide)
admin.site.register(GuideImage)
