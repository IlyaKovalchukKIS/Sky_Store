import datetime

from django.db import models

from blog.models import NULLABLE
from users.models import User


# Create your models here.

class Email(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок', **NULLABLE)
    text = models.TextField(max_length=1000, verbose_name='текст', **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Settings(models.Model):
    FREQUENCY_CHOICES = [
        ('1', 'Ежедневно'),
        ('7', 'Еженедельно'),
        ('30', 'Ежемесячно'),
    ]

    SENDING_TIME_CHOICES = [
        ('8', 'утро'),
        ('12', 'день'),
        ('19', 'вечер')
    ]

    STATUS_CHOICES = [
        ('created', 'создана'),
        ('completed', 'завершена'),
        ('launched', 'запущена')
    ]
    name = models.CharField(max_length=100, verbose_name='название')
    user = models.ManyToManyField(User, verbose_name='пользователи')
    sending_time = models.CharField(max_length=20, choices=SENDING_TIME_CHOICES, verbose_name='время рассылки')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, verbose_name='периодичность рассылки')
    start_time = models.DateTimeField(verbose_name='время начала рассылки', **NULLABLE)
    ending_time = models.DateTimeField(verbose_name='время окончания рассылки', **NULLABLE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='статус')
    message = models.ForeignKey(Email, on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE)

    def __str__(self):
        return f'{self.__class__.__name__}:({self.pk} {self.message.title})'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Log(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='кому')
    sent_datetime = models.DateTimeField(verbose_name='дата отправки', **NULLABLE)
    status = models.CharField(max_length=50, **NULLABLE, verbose_name='статус')
    response = models.TextField(**NULLABLE, verbose_name='ответ')
    email_settings = models.ForeignKey(Settings, on_delete=models.CASCADE, verbose_name='рассылка', **NULLABLE)

    def __str__(self):
        return f'{self.__class__.__name__}:({self.recipient} {self.sent_datetime} {self.status} {self.email_settings})'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
