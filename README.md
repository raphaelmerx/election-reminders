[![Build Status](https://travis-ci.org/raphaelmerx/election-reminders.svg?branch=master)](https://travis-ci.org/raphaelmerx/election-reminders)
[![Coverage Status](https://coveralls.io/repos/github/raphaelmerx/election-reminders/badge.svg?branch=master)](https://coveralls.io/github/raphaelmerx/election-reminders?branch=master)


# election-reminders

This project uses Python 3.5.1 and Django 1.9.1. The deployed environment uses Postgres and Redis as database backends,
     Celery for asynchronous tasks, Gunicorn for the HTTP server, and nginx for load balancing.

### Local setup:

* clone the repo
* if you don't have redis running, install it: [http://redis.io/topics/quickstart](http://redis.io/topics/quickstart)
* `pip install -r requirements/base.txt`
* `pip install -r requirements/test.txt`
* `cd election_reminders`
* `cp scripts/sample_env_vars ~/.election_reminders && source ~/.election_reminders`
* `./manage.py migrate`
* `PYTHONPATH=.: scripts/create_staff_user.py`
* `./manage.py fullserver`
* access the Django admin at [http://localhost:8000/admin](http://localhost:8000/admin)
