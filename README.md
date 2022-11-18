# Blog App

Blog App is a Django web app in which the user can sign up, sign in, create posts, like and comments etc.

## Installation
The first thing to do is to clone the repository:
```bash
git clone https://github.com/Amna-Laghari/BlogApp.git
```
Create a virtual environment to install dependencies in and activate it. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages from requirements.txt
```bash
pip install -r requirements.txt
```
Now run the server using command:
```bash
python manage.py runserver
```
## Versions
```bash
python_version = 3.10.7
Django = 4.1.3
```

## Dependencies
Following are the dependencies of the project. All of these are available in requirements.txt
```bash
asgiref==3.5.2
crispy-bootstrap5==0.7
dj-database-url==1.0.0
Django==4.1.3
django-ckeditor==6.5.1
django-cors-headers==3.13.0
django-crispy-forms==1.14.0
django-filter==22.1
django-js-asset==2.0.0
django-on-heroku==1.1.2
django-rest-framework==0.1.0
django-richtextfield==1.6.1
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.2
gunicorn==20.1.0
Jinja2==3.1.2
Markdown==3.4.1
MarkupSafe==2.1.1
Pillow==9.3.0
psycopg2-binary==2.9.5
PyJWT==2.6.0
pytz==2022.6
six==1.16.0
sqlparse==0.4.3
whitenoise==6.2.0
```
## Deployment

You can deploy the application on any online cloud platform for example heroku just make sure to migrate the database through following command.
```bash
puthon manage.py migrate
```

## Application Link

[BlogApp](http://blogapp213.herokuapp.com/)
