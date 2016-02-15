from celery import shared_task
from django.db import transaction

from .models import Schedule, Message


@shared_task
def create_messages():
    """ Create the messages for all upcoming elections.

    Also enqueue sending them.
    """
    for schedule in Schedule.objects.all():
        schedule.create_messages()  # noop if reminders already created
    for message in Message.objects.filter(sent=False):
        send_message.delay(message.id)


@shared_task
@transaction.atomic
def send_message(message_id):
    message = Message.objects.get(id=message_id)
    if message.sent:
        return
    if message.media_type == Schedule.EMAIL:
        message.send_email()
    elif message.media_type == Schedule.SMS:
        message.send_sms()

    message.sent = True
    message.save()
