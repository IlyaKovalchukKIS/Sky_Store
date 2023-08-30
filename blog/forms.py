from django import forms
from blog.models import Blog
from config.utils import StyleMixin


class BlogForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = Blog
        exclude = ('date_create', 'is_published', 'view_count', 'user', )
