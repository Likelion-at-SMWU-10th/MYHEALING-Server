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

    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:30]
