from datetime import date

from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings as email_name
from mailing.models import Settings, Log


def send_email():
    current_time = timezone.now()
    settings = Settings.objects.filter(status='launched', sending_time=current_time.time().hour).prefetch_related('user')

    for setting in settings:
        if not setting.start_time < current_time and not setting.ending_time > current_time:
            return

        recipients = setting.user.all()
        email_message = setting.message
        try:
            last_log = Log.objects.filter(email_settings=setting).last().sent_datetime.date
            sent = timezone.now().date - last_log

            if sent == setting.frequency:

                for recipient in recipients:
                    emailing(email_message, recipient, setting)
        except AttributeError:
            for recipient in recipients:
                emailing(email_message, recipient, setting)


def emailing(message, recipient, setting):
    email_message = message
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