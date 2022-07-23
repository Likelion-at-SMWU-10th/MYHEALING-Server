from xmlrpc.client import Boolean
from django.db import models

class Memory(models.Model):
    class Scope(models.TextChoices):
        PRIVATE = 'PRIVATE'
        PUBLIC = 'PUBLIC'

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField()
    place = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    body = models.TextField()
    scope = models.CharField(max_length=7, choices=Scope.choices, default=Scope.PRIVATE)
    thumbnail = models.IntegerField(default=-1)

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:30]

class MemoryImage(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE)
    # 'MEDIA_URL/img/memory/20220723/xxx.png' 문자열로 DB 필드 저장
    image = models.ImageField(upload_to = 'img/memory/%Y%m%d')
    