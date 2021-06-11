from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(auto_created=True)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=256)
    
    def __str__(self):
        return self.source
    
    class Meta:
        ordering = ['-date']
        
        
class Source(models.Model):
    
    name = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name