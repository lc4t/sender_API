### sender_API

#### Contribute

    every func is an app, commit one app as your function
    eg: express_tracking


`yourapp/init.py` is init your the db, I will exec it by `python manage.py shell`

and get the `function.id`, change `settings.py`, add your `function/ID` there

`python manage.py collectstatic` to get static files

after sync the db,

`rabbitmq-server` to start RabitMQ

`celery -A send_core worker --loglevel=info --beat` is how to start celery


change register status:

db: `send_core/status: register->invite`
