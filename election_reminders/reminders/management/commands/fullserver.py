import subprocess
import signal

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Starts runserver, celery and celerybeat.'

    def handle(self, *args, **options):
        processes = []

        print('Starting celery')
        processes.append(subprocess.Popen(['celery', 'worker', '-A', 'config']))
        print('Starting celerybeat')
        processes.append(subprocess.Popen(['celery', '-A', 'config', 'beat']))

        print('Starting runserver')
        processes.append(subprocess.Popen(['./manage.py', 'runserver']))

        try:
            signal.pause()
        except KeyboardInterrupt:
            pass

        print('Waiting for all processes to terminate...')
        [p.wait() for p in processes]
