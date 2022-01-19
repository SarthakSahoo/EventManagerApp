# EventManagerApp
This is a event management application which uses Graphene and Django as the backend. Different functionalities which are implemented are:
- Users can signup by providing their name, email and password (Email of user needs to be verified via Code sent to their email address)
- Users can log in using email/password OR code sent to their email address
- Users can create different types of events and invite others
- Authorized(Invited) users can start a comment thread on the event page
- Users will receive notifications on their email (with ICS file) for events


### Create a Virtual Environment
```virtualenv env```

### Activte the Virtual Environment
```source env/bin/activate```

### Install all the Dependencies
Please use the **requirements.txt** file to install all the required project dependencies

```pip install -r requirements.txt```

### Setting up the database
```python manage.py makemigrations```

```python manage.py migrate```

### Configure Email Backend

This email backend is defined with Gmail SMTP settings. You just need to add Gmail account and password.
- In gqldemo/settings.py add your GMAIL account to **EMAIL_HOST_USER** key.
- Don't add your original email password to **EMAIL_HOST_PASSWORD** key. Instead follow https://bit.ly/3rvRwTY and create app password and set that password to **EMAIL_HOST_PASSWORD** key.

Install RabbitMQ by following https://www.rabbitmq.com/download.html and ensure that RabbitMQ service is running.

### Start the Django server
```python manage.py runserver```

This will start the Django Server in the **port 8000**. Then you can start using the GraphQL by the endpoint

```http://localhost:8000/graphql```

### Start the Celery Worker
```celery -A gqldemo worker --loglevel=INFO```
