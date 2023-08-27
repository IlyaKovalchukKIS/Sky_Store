from django.db import models

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    body = models.CharField(verbose_name='содержимое')

    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    preview = models.ImageField(upload_to='preview/', verbose_name='изображение', **NULLABLE)
    date_create = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='опубликовано', default=True)
    view_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.title}, {self.view_count}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
