#!/usr/bin/env bash

sudo service gunicorn restart

CELERY_PID=$(cat celeryd.pid)
BEAT_PID=$(cat celerybeat.pid)

echo "Stopping celery"
kill $CELERY_PID
while [ -x /proc/${CELERY_PID} ]
do
    echo "Waiting for celery to shutdown ..."
    sleep 1
done
echo "Celery stopped"

echo "Stopping celery beat"
kill $BEAT_PID
while [ -x /proc/${BEAT_PID} ]
do
    echo "Waiting for celery beat to shutdown ..."
    sleep 1
done
echo "Celery beat stopped"

celery worker -A config --detach --logfile /var/log/celery/worker.log
celery -A config beat --detach  --logfile /var/log/celery/beat.log
