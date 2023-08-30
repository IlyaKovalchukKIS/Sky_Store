from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from config.utils import StyleMixin

from users.models import User


class UserRegisterForm(StyleMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email',  'country', 'password1', 'password2',)


class UserProfileForm(StyleMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
