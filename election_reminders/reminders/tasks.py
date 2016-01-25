from celery import shared_task
from django.core.mail import send_mail

from .models import Schedule, Message


@shared_task
def create_messages():
    for schedule in Schedule.objects.all():
        schedule.create_reminders()
    for message in Message.objects.filter(sent=False):
        send_message.delay(message.id)


@shared_task
def send_message(message_id):
    message = Message.objects.get(id=message_id)
    if message.sent:
        return
    dest = message.voter.user.email
    send_mail(subject='Hey there', message='Body of the message', from_email='election@reminders.com', recipient_list=[dest], fail_silently=False)
    message.sent = True
    message.save()
