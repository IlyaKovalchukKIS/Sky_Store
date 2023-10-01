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


class UserBlock(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} {self.is_blocked}'

    class Meta:
        verbose_name = 'блокировка пользователя'
        verbose_name_plural = 'блокировки пользователей'
        permissions = [
            (
                'is_blocked',
                'Can blocked users'
            )
        ]