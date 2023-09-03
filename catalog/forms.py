from django import forms
from catalog.models import Product, Category, Version
from config.utils import StyleMixin


class ProductForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('date_create', 'view_count', 'user', 'is_active')

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        for word in self.forbidden_words:
            if word in name.lower() or word in description.lower():
                raise forms.ValidationError(f'В названии или в описании использовано запрещенное слово')
        return cleaned_data


class CategoryForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        for word in self.forbidden_words:
            if word in name.lower() or word in description.lower():
                raise forms.ValidationError(f'В названии или в описании использовано запрещенное слово')
        return cleaned_data


class VersionForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Version
        exclude = ('is_active',)
