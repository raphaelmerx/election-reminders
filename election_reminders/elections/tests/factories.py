from datetime import datetime

import pytz
from factory.django import DjangoModelFactory

from elections.models import Election


class ElectionFactory(DjangoModelFactory):
    class Meta:
        model = Election

    date = datetime(2016, 3, 1, 9, 00, 00, tzinfo=pytz.timezone('America/New_York'))
    name = 'Virginia Primary election'
    state = 'VA'
