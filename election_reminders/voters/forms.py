from django.forms import ModelForm

from .models import Voter


class UnsubscribeForm(ModelForm):
    class Meta:
        model = Voter
        fields = ['unsubscribed']
