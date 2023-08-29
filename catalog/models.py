from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='preview/', verbose_name='изображение', **NULLABLE)
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    date_last_change = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.CharField(max_length=150, verbose_name='описание')
    preview = models.ImageField(upload_to='preview/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.IntegerField(verbose_name='цена')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    date_last_change = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.category}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('price',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар')
    version = models.IntegerField(verbose_name='номер версии')
    name_version = models.CharField(max_length=100, verbose_name='название версии')
    is_active = models.BooleanField(default=True, verbose_name='активна')

    def __str__(self):
        return f'{self.product.name} {self.version} {self.is_active}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
