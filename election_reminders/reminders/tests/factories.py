from datetime import timedelta

import factory
from factory.django import DjangoModelFactory

from reminders.models import Message, Schedule
from voters.tests.factories import VoterFactory
from elections.tests.factories import ElectionFactory


class ScheduleFactory(DjangoModelFactory):
    class Meta:
        model = Schedule

    media_type = Schedule.EMAIL
    time_before_election = timedelta(days=1)


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    media_type = Schedule.EMAIL
    schedule = factory.SubFactory(ScheduleFactory)
    voter = factory.SubFactory(VoterFactory)
    election = factory.SubFactory(ElectionFactory)
