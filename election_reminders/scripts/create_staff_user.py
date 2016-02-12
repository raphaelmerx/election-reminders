#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.auth.models import User
from django.conf import settings


if settings.DEBUG != True:
    raise Exception('Cannot create a default staff in a deployed environment')
u, _ = User.objects.get_or_create(username='staff', is_staff=True, is_superuser=True)
u.set_password('1234')
u.save()
