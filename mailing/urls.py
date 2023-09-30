from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MessageCreateView, MessageUpdateView, MessageDeleteView, MessageListView, MessageDetailView, \
    SettingsCreateView, SettingsListView, SettingsDetailView, SettingsUpdateView, SettingsDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('create/', MessageCreateView.as_view(), name='mailing_create'),
    path('list/', MessageListView.as_view(), name='message_list'),
    path('detail/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('settings/create/', SettingsCreateView.as_view(), name='settings_create'),
    path('settings/list/', SettingsListView.as_view(), name='settings_list'),
    path('settings/detail/<int:pk>', SettingsDetailView.as_view(), name='settings_detail'),
    path('settings/update/<int:pk>', SettingsUpdateView.as_view(), name='settings_update'),
    path('settings/delete/<int:pk>', SettingsDeleteView.as_view(), name='settings_delete'),

]
