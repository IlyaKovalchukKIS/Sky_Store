from django import forms
from config.utils import StyleMixin
from mailing.models import Email, Settings


class MailingForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Email
        fields = '__all__'


class SettingsMailForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Settings
        fields = '__all__'


class SettingsStatusForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = Settings
        fields = ('status',)
