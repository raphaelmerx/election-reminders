from datetime import datetime

import pytz
from django.db import models

from voters.models import Voter
from elections.models import Election


class Schedule(models.Model):
    """ Used to set how much time before elections a message should be sent. """
    time_before_election = models.DurationField(
        help_text='Ex: 2 days to send a reminder 2 days before all elections.'
                  'Format is "days hours:min:secs". Ex: "1 02:00:00" for one day, 2 hours before.')
    EMAIL = 'E'
    SMS  = 'S'
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
