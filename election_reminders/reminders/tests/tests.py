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
