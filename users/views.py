import os
import random

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Permission
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.views import LoginView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User, UserBlock

product_permissions = ['catalog.add_product', 'catalog.change_product']


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    @staticmethod
    def send_email_func(email_user):
        send_mail(
            subject='Поздравляю',
            message='Welcome',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email_user],
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD
        )

    def form_valid(self, form):
        permissions = ['add_product', 'change_product']
        new_user = form.save()
        for perm in permissions:
            perm_user: Permission = Permission.objects.get(codename=perm)
            new_user.user_permissions.add(perm_user)
        block_create = UserBlock.objects.create(user=new_user)
        block_create.save()

        new_user.save()
        self.send_email_func(new_user.email)

        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_blocks = UserBlock.objects.select_related('user').all()
        context['user_data'] = [{'user': block.user, 'is_blocked': block} for block in user_blocks]
        return context


class UserBlockView(UserPassesTestMixin, UpdateView):
    model = UserBlock
    fields = ('is_blocked',)
    template_name = 'users/user_blocked_form.html'
    success_url = reverse_lazy('users:all_users_register')

    def test_func(self):
        return self.request.user.has_perm('users.is_blocked')
