from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from twilio.rest import TwilioRestClient
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
    if message.media_type == Message.EMAIL:
        # TODO: Use mandrill
        dest = message.voter.user.email
        send_mail(subject='Hey there', message='body', from_email='election@reminders.com', recipient_list=[dest], fail_silently=False)
    elif message.media_type == Message.SMS:
        # TODO: put this logic in the models
        twilio_client = TwilioRestClient(settings.TWILIO_ACCOUNT_ID, settings.TWILIO_TOKEN)
        # TODO: format election.date according to the voter's timezone
        twilio_client.messages.create(
            to=message.voter.phone_number,
            from_='+14807718683',
            body='The {} will be held on {:%m/%d/%y} at {:%I%p}.'.format(
                message.election.name, message.election.date, message.election.date)
        )

    message.sent = True
    message.save()
