from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = CountryField(verbose_name='страна', **NULLABLE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
