from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(auto_created=True)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=256)
    
    def __str__(self):
        return self.category
    
    class Meta:
        ordering = ['-date']
        
        
class Category(models.Model):
    name = models.CharField(max_length=256)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name