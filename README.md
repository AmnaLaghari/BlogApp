# Blog App

Blog App is a Django web app in which the user can sign up, sign in, create posts, like and comments etc.

## Setup
The first thing to do is to clone the repository:
```bash
git clone https://github.com/Amna-Laghari/BlogApp.git
```
Create a virtual environment to install dependencies in and activate it.
```bash
virtualenv2 --no-site-packages env
source env/bin/activate
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages from requirements.txt
```bash
pip install -r requirements.txt
```
Once pip has finished downloading the dependencies
```bash
cd project
python manage.py runserver
```
## Versions
```bash
python_version = 3.10.7
Django = 4.1.3
```
## Deployment

You can deploy the application on any online cloud platform for example heroku just make sure to migrate the database through following command.
```bash
python manage.py migrate
```

## Application Link

[BlogApp](http://blogapp213.herokuapp.com/)
