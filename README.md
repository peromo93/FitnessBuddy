# FitnessBuddy

FitnessBuddy is a diet and fitness tracking single page application. It is built using AngularJS, Django REST Framework, and Bootstrap. Users can log their daily food intakes and monitor their nutrition and weight goals. Food nutrition information is provided by the [USDA Food Composition Database](https://ndb.nal.usda.gov/ndb/).

This project is a work in progress.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

Install the required packages listed in requirements.txt:

```
$ pip install -r requirements.txt
```

### Configuration

Before running the server for the first time, we need to create the database tables from Django models.

Create new migrations for all of our apps (note that we will generate a new secret key if one does not already exist):

```
$ python manage.py makemigrations foodlog users
Migrations for 'users':
  users/migrations/0001_initial.py
    - Create model Profile
Migrations for 'foodlog':
  foodlog/migrations/0001_initial.py
    - Create model DailyLog
    - Create model FoodEntry
```

Then apply the current set of migrations:

```
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, foodlog, sessions, users
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying users.0001_initial... OK
  Applying foodlog.0001_initial... OK
  Applying sessions.0001_initial... OK
```

### Running the Server

Run the following command to run the Django server:

```
$ python manage.py runserver
Using USDA NDB Demo API key.
Performing system checks...

System check identified no issues (0 silenced).
July 19, 2017 - 03:37:49
Django version 1.11.2, using settings 'FitnessBuddy.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

If there are no errors, open a browser and visit http://127.0.0.1:8000. Congratulations, you are now running a local instance of FitnessBuddy!

## Built With

* [Python 2.7.12](https://www.python.org/downloads/release/python-2712/)
* [AngularJS 1.6.4](https://angularjs.org/) - Front-end web framework
* [angular-jwt](https://github.com/auth0/angular-jwt) - AngularJS library for JWT authentication
* [Django 1.11](https://docs.djangoproject.com/en/1.11/releases/1.11/) - Back-end web framework
* [Django REST Framework 3.6](http://www.django-rest-framework.org/topics/3.6-announcement/) - Back-end REST framework
* [Django REST Framework JWT](https://github.com/GetBlimp/django-rest-framework-jwt) - DRF library for JWT authentication
* [Bootstrap 4](https://v4-alpha.getbootstrap.com/) - Front-end web framework
* [Font Awesome 3.2.1](http://fontawesome.io/3.2.1/icons/) - Vector icon toolkit
* [jQuery 3.2.1](https://blog.jquery.com/2017/03/20/jquery-3-2-1-now-available/) - JavaScript library

## Authors

* **Peter R** - [peromo93](https://github.com/peromo93)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
