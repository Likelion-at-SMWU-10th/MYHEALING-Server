from django.db import models

# Create your models here.
class Guide(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    buy = models.CharField(max_length=50, blank=True) # 구매 여부(해당사항 없다면 작성하지 않아도 됨.)
    body = models.TextField()

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:30]