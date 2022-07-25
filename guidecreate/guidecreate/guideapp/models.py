from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Guide(models.Model):
    creator_id = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True) # auto_now_add는 임시로 지정해둔 것
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    place = models.CharField(max_length=50, default = '')
    cost = models.CharField(max_length=50, blank=True) # 구매 여부(해당사항 없다면 작성하지 않아도 됨)
    title = models.CharField(max_length=50)
    body = models.TextField()
    address = models.CharField(max_length=50, default = '')
    views = models.IntegerField(default = 0)
    thumbnail = models.ImageField(upload_to='guideapp/img', height_field=None, width_field=None, max_length=100, blank=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:30]