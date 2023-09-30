from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView, CreateView

from mailing.forms import MailingForm, SettingsMailForm
from mailing.models import Settings, Email, Log


# Create your views here.


class MessageCreateView(CreateView):
    model = Email
    form_class = MailingForm
    success_url = reverse_lazy('mailing:message_list')


class MessageListView(ListView):
    model = Email


class MessageDetailView(DetailView):
    model = Email


class MessageUpdateView(UpdateView):
    model = Email
    form_class = MailingForm
    template_name = 'mailing/email_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView):
    model = Email


# Настройки рассылки
class SettingsCreateView(CreateView):
    form_class = SettingsMailForm
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


class SettingsUpdateView(UpdateView):
    form_class = SettingsMailForm
    model = Settings
    success_url = reverse_lazy('mailing:settings_list')


class SettingsDeleteView(DeleteView):
    model = Settings
