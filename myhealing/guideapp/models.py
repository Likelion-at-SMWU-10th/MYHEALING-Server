from unittest.util import _MAX_LENGTH
from django.db import models
from accounts.models import User

# Create your models here.
class Guide(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guide")
    date = models.DateField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    place = models.CharField(max_length=50, default = '')
    cost = models.IntegerField()
    title = models.CharField(max_length=50)
    body = models.TextField()
    address = models.CharField(max_length=50, default = '')
    views = models.IntegerField(default = 0)
    tag = models.ManyToManyField('Tag', related_name='guide')

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:30]

class Love(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name="love")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="love")
    created_at = models.DateTimeField(auto_now_add=True)

class GuideImage(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name="images")

    def image_upload_path(instance, filename):
        return 'img/guide/{0}/{1}'.format(instance.guide.id, filename)
    
    image = models.ImageField(upload_to = image_upload_path)
    thumbnail = models.BooleanField(default=False)

class Tag(models.Model):
    class Sort(models.TextChoices):
        MOOD = 'MOOD'
        WEATHER = 'WEATHER'
        WHO = 'WHO'
        REGION = 'REGION'
        ETC = 'ETC'
    
    sort = models.CharField(max_length=7, choices=Sort.choices, default=Sort.ETC)
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title

class RandomGuide(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title