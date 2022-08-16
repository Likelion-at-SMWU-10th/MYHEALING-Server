from xmlrpc.client import Boolean
from django.db import models
from accounts.models import User

class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memory")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField()
    place = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    body = models.TextField()
    address = models.CharField(max_length=50, default = '')

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:30]

class MemoryImage(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name="images")

    def image_upload_path(instance, filename):
        return 'img/memory/{0}/{1}'.format(instance.memory.id, filename)

    # 'MEDIA_URL/img/memory/2022/07/23/{memory.pk}/xxx.png' 문자열로 DB 필드 저장
    image = models.ImageField(upload_to = image_upload_path)
    thumbnail = models.BooleanField(default=False)
    
    