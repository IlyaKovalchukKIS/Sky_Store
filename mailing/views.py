from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView

from mailing.forms import MailingForm, SettingsMailForm, SettingsStatusForm
from mailing.models import Settings, Email, Log
from users.models import User


# Create your views here.


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Email
    form_class = MailingForm
    permission_required = 'mailing.add_email'
    success_url = reverse_lazy('mailing:message_list')


class MessageListView(ListView):
    model = Email


class MessageDetailView(DetailView):
    model = Email


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Email
    form_class = MailingForm
    permission_required = 'mailing.change_email'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Email
    permission_required = 'mailing.delete_email'


# Настройки рассылки
class SettingsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = SettingsMailForm
    permission_required = 'mailing.add_settings'
    model = Settings
    success_url = reverse_lazy('mailing:settings_list')


class SettingsListView(ListView):
    model = Settings


class SettingsDetailView(DetailView):
    model = Settings
    context_object_name = 'settings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        users = self.object.user.all()

        last_logs = {}
        for user in users:
            last_log = Log.objects.filter(recipient=user, email_settings=self.object).order_by('-sent_datetime').first()
            if last_log:
                last_logs[user] = last_log

        context['last_logs'] = last_logs
        return context


class SettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = SettingsMailForm
    permission_required = 'mailing.change_settings'
    model = Settings
    success_url = reverse_lazy('mailing:settings_list')

    def get_form_class(self):
        if self.request.user.groups.filter(name='manager').exists():
            return SettingsStatusForm
        else:
            return super().get_form_class()


class SettingsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Settings
    permission_required = 'mailing.delete_settings'

