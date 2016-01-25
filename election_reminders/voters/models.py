from django.conf import settings
from django.db import models


class Voter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unsubscribed = models.BooleanField(default=False)
    street_address = models.CharField(max_length=127, help_text='Ex: 123 Brown St')
    city = models.CharField(max_length=64, help_text='Ex: New York City')
    state = models.CharField(max_length=2, help_text='2 letter upper case state code. Ex: VA')
