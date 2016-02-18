import factory
from factory.django import DjangoModelFactory
from django.conf import settings

from voters.models import Voter


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: 'john_{}'.format(n))
    first_name = 'John'
    email = factory.LazyAttribute(lambda u: '{0.username}@gmail.com'.format(u))


class VoterFactory(DjangoModelFactory):
    class Meta:
        model = Voter

    user = factory.SubFactory(UserFactory)
    street_address = '123 Montgomery St'
    city = 'San Francisco'
    state = 'CA'
    phone_number = '+14444444444'
