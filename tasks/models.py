from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model

# Create your models here.

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Para usuarios administradores
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'  # Este campo será el que se usará para login
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']  # Campos obligatorios para crear un usuario

    def __str__(self):
        return self.username
    
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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='')
    
    def __str__(self):
        return self.title + ' - by ' + self.user.username