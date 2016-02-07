from datetime import datetime

import pytz
from factory.django import DjangoModelFactory

from elections.models import Election


class ElectionFactory(DjangoModelFactory):
    class Meta:
        model = Election

    # 9AM + 5 for UTC
    date = datetime(2016, 3, 1, 14, 00, 00, tzinfo=pytz.utc)
    name = 'Virginia Primary election'
    state = 'VA'
