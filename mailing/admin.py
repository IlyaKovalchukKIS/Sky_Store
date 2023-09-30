from django.contrib import admin

from mailing.models import Log


# Register your models here.


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'sent_datetime', 'status', 'response', 'email_settings',)
