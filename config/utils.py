class StyleMixin:
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
        self.forbidden_words = self.__forbidden_words
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'