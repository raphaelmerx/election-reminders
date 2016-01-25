from django.db import models


class Election(models.Model):
    date = models.DateTimeField(help_text='When this election will be held.', db_index=True)
    name = models.CharField(blank=False, max_length=255, help_text='A user friendly name.')
    state = models.CharField(blank=True, max_length=2, help_text='A 2 letter representation of the state. Blank if national election.')
