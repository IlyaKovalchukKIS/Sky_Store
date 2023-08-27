from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='preview/', verbose_name='изображение', **NULLABLE)
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    date_last_change = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')

    def __str__(self):
        return f'{self.name} {self.date_creation}'

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

    def __str__(self):
        return f'{self.name} {self.category}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('price',)
