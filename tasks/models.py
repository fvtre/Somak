from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    CATEGORY_CHOICES = [
        ('home', 'Home'),
        ('casadepaz', 'Casa de Paz'),
        ('aviva2', 'Aviva2'),
        ('avivakids', 'Avivakids'),
        ('jovenes', 'Jovenes'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='')
    
    def __str__(self):
        return self.title + ' - by ' + self.user.username