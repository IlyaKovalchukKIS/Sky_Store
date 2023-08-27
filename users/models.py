from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    COUNTRY_CHOICES = [
        ('1', 'Russia'),
        ('2', 'USA'),
        ('3', 'Germany',),
        ('4', 'Austria',),
        ('5', 'Africa',),
    ]
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=150, verbose_name='страна', choices=COUNTRY_CHOICES, **NULLABLE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
