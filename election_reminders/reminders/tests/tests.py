from unittest import mock
from datetime import timedelta, datetime

import pytz
from django.test import TestCase, override_settings
from django.core import mail

from elections.tests.factories import ElectionFactory
from voters.models import Voter
from voters.tests.factories import VoterFactory
from reminders.tests.factories import ScheduleFactory
from reminders.models import Message
from reminders.tasks import create_messages, send_message
from .factories import MessageFactory


class CreateMessage(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = datetime.now(pytz.utc)
        election = ElectionFactory(date=now + timedelta(hours=18))
        VoterFactory(state=election.state)
        ScheduleFactory()

    def test_should_create_message(self):
        self.assertEqual(Message.objects.count(), 0)
        create_messages()
        self.assertEqual(Message.objects.count(), 1)

    def test_no_message_for_voter_in_other_state(self):
        Voter.objects.all().update(state='WA')
        self.assertEqual(Message.objects.count(), 0)
        create_messages()
        self.assertEqual(Message.objects.count(), 0)

    def test_dont_create_message_twice(self):
        """ If the create_messages task runs twice, don't create duplicate messages. """
        self.assertEqual(Message.objects.count(), 0)
        create_messages()
        self.assertEqual(Message.objects.count(), 1)
        create_messages()
        self.assertEqual(Message.objects.count(), 1)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_no_email_sent_if_message_sent(self):
        message = MessageFactory(sent=False)
        send_message(message.id)
        self.assertEqual(len(mail.outbox), 1)

        message.refresh_from_db()
        self.assertTrue(message.sent)
        # message is sent now, don't resend an email
        send_message(message.id)
        self.assertEqual(len(mail.outbox), 1)

class SendMessages(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_truc(self):
        with mock.patch('reminders.tasks.TwilioRestClient') as mock_twilio:
            # set the TwilioRestClient instance so that we use the same object here and in the reminders.tasks module
            twilio_instance = mock.Mock()
            mock_twilio.return_value = twilio_instance
            send_sms = twilio_instance.messages.create
            self.assertEqual(send_sms.call_count, 0)
            message = MessageFactory(media_type=Message.SMS, voter__phone_number='+2222222222')
            send_message.delay(message.id)
            self.assertEqual(send_sms.call_count, 1)
            self.assertEqual(send_sms.call_args[1]['body'],
                             'The Virginia Primary election will be held on 03/01/16 at 01PM.')
