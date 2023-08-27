from django import forms
from catalog.models import Product, Category


class ProductForm(forms.ModelForm):
    __forbidden_words = ['казино',
                         'криптовалюта',
                         'крипта',
                         'биржа',
                         'дешево',
                         'бесплатно',
                         'обман',
                         'полиция',
                         'радар']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        for word in self.__forbidden_words:
            if word in name.lower() or word in description.lower():
                raise forms.ValidationError(f'В названии или в описании использовано запрещенное слово')
        return cleaned_data


class CategoryForm(forms.ModelForm):
    __forbidden_words = ['казино',
                         'криптовалюта',
                         'крипта',
                         'биржа',
                         'дешево',
                         'бесплатно',
                         'обман',
                         'полиция',
                         'радар']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Category
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')

        for word in self.__forbidden_words:
            if word in name.lower() or word in description.lower():
                raise forms.ValidationError(f'В названии или в описании использовано запрещенное слово')
        return cleaned_data
