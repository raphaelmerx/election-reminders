# election-reminders

This project uses Python 3.5.1 and Django 1.9.1.

Local setup:
* clone the repo
* `pip install -r requirements/base.txt`
* `pip install -r requirements/test.txt`
* `cd election_reminders`
* `./manage.py migrate`
* `PYTHONPATH=.: scripts/create_staff_user.py`
* `./manage.py runserver`
* access the Django admin at [http://localhost:8000/admin](http://localhost:8000/admin)
