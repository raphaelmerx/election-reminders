from django.db import models


class Election(models.Model):
    date = models.DateTimeField(help_text='When this election will be held.', db_index=True)
    name = models.CharField(blank=False, max_length=255, help_text='User friendly name., eg Virginia Primary Election')
    state = models.CharField(blank=True, max_length=2, help_text='2 letter representation of the state. Blank if national election.')

    def __str__(self):
        return self.name
