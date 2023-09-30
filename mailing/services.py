from datetime import date

from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings as email_name
from mailing.models import Settings, Log


def send_email():
    current_time = timezone.now().time().hour
    settings = Settings.objects.filter(status='created', sending_time=current_time).prefetch_related('user')

    for setting in settings:
        last_log = Log.objects.filter(email_settings=setting).last().sent_datetime.date
        sent = timezone.now().date - last_log
        if sent == setting.frequency:
            continue

        recipients = setting.user.all()
        email_message = setting.message

        for recipient in recipients:
            try:
                send_mail(
                    email_message.title,
                    email_message.text,
                    email_name.EMAIL_HOST_USER,
                    [recipient.email],
                    fail_silently=False,
                )
                status = 'Отправлено'
                response = ''
            except Exception as e:
                status = 'Ошибка'
                response = str(e)

            log = Log.objects.create(
                recipient=recipient,
                sent_datetime=timezone.now(),
                status=status,
                response=response,
                email_settings=setting
            )
            log.save()