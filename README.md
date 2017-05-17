### sender_API

#### Contribute

    every func is an app, commit one app as your function
    eg: express_tracking


1. learn `Django`, create your app
2. `yourapp/init.py` is init your the db, I will exec it by `python manage.py shell`
3. and get the `function.id` from db, change `settings.py`, add your `function/ID` there
4. user delete callback: `func.delete(task)`
5. user ajax request: check `urls.py`, named `function/ID/ajax`
6. `tasks.py` is where you commit your tasks

#### Build

`python manage.py collectstatic` to get static files

`python manage.py migrate` to sync db, after you set db config in `settings.py`

`rabbitmq-server` to start RabitMQ

`celery -A send_core worker --loglevel=info --beat` is how to start celery


if you want to change register status:

on db(Django Admin): `send_core/status: register->invite`

`python manage.py createsuperuser` to create an admin user.

`python manage.py runserver` to run.


Refer: [MyBlog](https://lc4t.github.io/2017/05/17/Sender%E9%83%A8%E7%BD%B2/)
