import random

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from pytils.translit import slugify

from config import settings


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


class ViewMixin:

    def form_valid(self, form):
        image = self.request.FILES.get('image')
        if image:
            new_object = form.save(commit=False)
            new_object.image = image
            new_object.save()
        else:
            form.save()

        if form.is_valid():
            new_object = form.save()

            if hasattr(new_object, 'slug'):
                new_object.slug = slugify(new_object.title)

            new_object.user = self.request.user
            new_object.save()

        return super().form_valid(form)


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        auth_user=settings.EMAIL_HOST_USER,
        auth_password=settings.EMAIL_HOST_PASSWORD,
    )

    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:index'))
