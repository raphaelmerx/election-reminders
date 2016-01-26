from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator


class Voter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unsubscribed = models.BooleanField(default=False)
    street_address = models.CharField(max_length=127, help_text='Ex: 123 Brown St')
    city = models.CharField(max_length=64, help_text='Ex: New York City')
    state = models.CharField(max_length=2, help_text='2 letter upper case state code. Ex: VA')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be entered in the format: +99999999.')
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=16)
