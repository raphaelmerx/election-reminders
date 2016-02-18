from unittest import mock
from datetime import timedelta, datetime
from contextlib import contextmanager

import pytz
from django.test import TestCase, override_settings
from django.core import mail
from djrill.mail.backends.djrill import DjrillBackend

from elections.factories import ElectionFactory
from voters.models import Voter
from voters.factories import VoterFactory
from reminders.factories import ScheduleFactory
from reminders.models import Message, Schedule
from reminders.tasks import create_messages, send_message
from .factories import MessageFactory


@contextmanager
def mock_twilio():
    with mock.patch('reminders.models.TwilioRestClient') as mock_twilio:
        # set the TwilioRestClient instance so that we use the same object here and in the reminders.models module
        twilio_instance = mock.Mock()
        mock_twilio.return_value = twilio_instance
        yield twilio_instance


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


class SendMessages(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.message = MessageFactory(schedule__media_type=Schedule.SMS)
        cls.email_message = MessageFactory(schedule__media_type=Schedule.EMAIL)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_created_message_sent_with_twilio(self):
        with mock_twilio() as twilio_client:
            send_sms = twilio_client.messages.create
            self.assertEqual(send_sms.call_count, 0)
            send_message.delay(self.message.id)
            self.assertEqual(send_sms.call_count, 1)

    def test_show_election_time_in_election_timezone(self):
        with mock_twilio() as twilio_client:
            # hour in UTC
            self.assertEqual(self.message.election.date.hour, 14)
            send_sms = twilio_client.messages.create
            self.message.send_sms()
            self.assertEqual(send_sms.call_count, 1)
            self.assertEqual(send_sms.call_args[1]['body'],
                             'The Virginia Primary election will be held on 03/01/16 at 09AM.')

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_no_email_sent_if_message_already_sent(self):
        message = self.email_message
        send_message(message.id)
        self.assertEqual(len(mail.outbox), 1)

        message.refresh_from_db()
        self.assertTrue(message.sent)
        send_message(message.id)
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(EMAIL_BACKEND='djrill.mail.backends.djrill.DjrillBackend')
    def test_send_email(self):
        message = self.email_message
        with self.mock_mandrill(message) as email:
            self.assertIn('The Virginia Primary election will be held on 03/01/16 at 09AM.', email.body)

    @override_settings(EMAIL_BACKEND='djrill.mail.backends.djrill.DjrillBackend')
    def test_unsubscribe_link_in_email(self):
        message = self.email_message
        with self.mock_mandrill(message) as email:
            # in header
            unsubscribe_url = email.extra_headers['List-Unsubscribe'][1:-1]
            self.assertEqual(unsubscribe_url, message.unsubscribe_url)
            self.assertIn(str(message.voter.uuid), unsubscribe_url)

            # in email body
            self.assertIn(message.unsubscribe_url, email.body)

    @contextmanager
    def mock_mandrill(self, message):
        with self.settings(EMAIL_BACKEND='djrill.mail.backends.djrill.DjrillBackend'), \
                mock.patch.object(DjrillBackend, 'send_messages') as mock_send_messages:
            message.send_email()
            self.assertTrue(mock_send_messages.called)
            email = mock_send_messages.call_args[0][0][0]
            yield email
