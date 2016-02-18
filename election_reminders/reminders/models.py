import urllib
from datetime import datetime

import us
import pytz
from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from twilio.rest import TwilioRestClient

from voters.models import Voter
from elections.models import Election


class Schedule(models.Model):
    """ Used to set how much time before elections a message should be sent. """
    time_before_election = models.DurationField(
        help_text='Ex: 2 days to send a reminder 2 days before all elections.'
                  'Format is "days hours:min:secs". Ex: "1 02:00:00" for one day, 2 hours before.')
    EMAIL = 'E'
    SMS = 'S'
    MEDIA_TYPE_CHOICES = (
        (EMAIL, 'email'),
        (SMS, 'SMS'),
    )
    media_type = models.CharField(max_length=2, choices=MEDIA_TYPE_CHOICES)

    def create_messages(self):
        """ Create reminders corresponding to this schedule.

        idempotent: if the messages are already created, this method won't create duplicates
        Does not send the messages.
        """
        now = datetime.now(pytz.utc)
        upcoming_elections = Election.objects.filter(date__range=(now, now + self.time_before_election))
        for election in upcoming_elections:
            location_filter = {'state': election.state} if election.state else {}
            if Message.objects.filter(election=election, schedule=self).exists():
                # messages for this election and schedule already exist
                continue
            Message.objects.bulk_create(
                [Message(election=election, schedule=self, voter=voter, sent=False)
                 for voter in Voter.objects.filter(**location_filter)])


class Message(models.Model):
    """ An email or a SMS that was sent based on an election and a Schedule. """
    sent = models.BooleanField(default=False)
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    @property
    def media_type(self):
        return self.schedule.media_type

    def send_sms(self):
        assert self.media_type == Schedule.SMS

        twilio_client = TwilioRestClient(settings.TWILIO_ACCOUNT_ID, settings.TWILIO_TOKEN)
        tz_name = getattr(us.states, self.election.state).time_zones[0]
        date_in_election_tz = self.election.date.astimezone(tz=pytz.timezone(tz_name))
        twilio_client.messages.create(
            to=self.voter.phone_number,
            from_='+14807718683',
            body='The {} will be held on {:%m/%d/%y} at {:%I%p}.'.format(
                self.election.name, date_in_election_tz, date_in_election_tz)
        )

    @property
    def unsubscribe_url(self):
        # TODO: use the Django site object
        return ('https://electionreminders.org' + reverse('unsubscribe') +
                '?' + urllib.parse.urlencode({'uuid': self.voter.uuid}))

    def send_email(self):
        assert self.media_type == Schedule.EMAIL

        tz_name = getattr(us.states, self.election.state).time_zones[0]
        election_tz = pytz.timezone(tz_name)
        date_in_election_tz = self.election.date.astimezone(tz=election_tz).strftime('%m/%d/%y at %I%p')
        unsubscribe_url = self.unsubscribe_url
        template_data = {'first_name': self.voter.user.first_name,
                         'election_name': self.election.name,
                         'date': date_in_election_tz,
                         'unsubscribe_url': unsubscribe_url}
        text_body = render_to_string('email.txt', template_data)
        html_body = render_to_string('email.html', template_data)
        headers = {'List-Unsubscribe': '<{}>'.format(unsubscribe_url)}
        email = EmailMultiAlternatives(
            subject='An election is coming up!', from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.voter.user.email], body=text_body, headers=headers)
        email.attach_alternative(html_body, 'text/html')
        email.send()
