## Steps to setup django
### don't forget to workon "evn" when logged into vagrant server
### in local directory
- install virtualbox
- install vagrant, vagrant init, & use vagrantfile to determine OS
- mkdir src
- touch .gitignore (add python ignore from github)
- vagrant up to run server
- vagrant ssh to login to server
### in vagrant server:   
- mkvirtualenv "env name" --python=python3
- (deactivate / workon "env name")
- pip install django=="version"
- pip install djangorestframework=="version"
- cd /vagrant/src
- django-admin.py startproject "project name"
- cd "project-name"
- python manage.py startapp "app name"

### add apps
- open src >project_dir >project_dir >settings.py 
- add apps to INSTALLED_APPS list
    - rest_framework
    - rest_framework.authtoken
    - "app_name"
### create requirements file
- in vagrant server, logged in to virtualenv, in /vagrant/ folder:
- pip freeze (view packages installed)
- pip freeze > requirements.txt

### run test server
- in vagrant server, logged into virtualenv:
- cd /vagrant/src/"project name"
- python manage.py runserver 0.0.0.0:8080
- This runs the server on all ip's, out of port 8080. This means on the local computer, the server will be accessible at the ip address specified in the vagrantfile

### creating models
- creating the models: see models.py file for example
- update settings.py to update any defaults to the new one (like default user model)
- in vagrant server, logged into virtualenv:
- cd /vagrant/src/"project name"
- python manage.py makemigrations (creates the blueprint for updating the database with the model)
- python manage.py migrate (creates the database)

### django admin
- create a superuser: python manage.py createsuperuser
- register superuser in admin.py file of api app:
- in admin.py:
    - from . import models
    - admin.site.register(UserProfile)

### API Views
The next segments will explain how APIView is used
- open views.py file in application directory
- Imports:
    - from rest_framework.views import APIView
    - from rest_framework.response import Response
- define classes for view responses
- map url to view:
- in urls.py for the project,
    - import include: from django.conf.urls import include
    - add url pattern to list and map to the app urls file using the include call
- create the urls file in the app directory
    - from django.conf.urls import url
    - from . import views
    - define url patterns w/ views

### Create Serializer & POST
- create file called serializers.py in application direcotry
- import serializers from DRF
    - from rest_framework import serializers
- define serialize function
- now add it to the view, in apps view.py file:
    - import serilizer file: from . import serializers
    - add post function w/ any desired validation

### Add remaining REST functions
- in views.py within application directory:
- create put function

### Viewsets
This segment will show how to use viewsets instead of API View  
Allows List, create, retrieve, update, partial update and destroy

- import viewsets from rest_framework in views.py
- create desired class, and define a function (such as list)
- in urls.py within api app, import rest_framework DefaultRouter
- define the router from the import, and register it with a name and the desired view
- add the url to the url pattern list (still in urls.py)

### permissions
- restricts any user from updating any other users' profile
- create a permissions.py file in api app
- import permissions from rest framework
- create a class to validate user requesting a change is the owner of the object being changed
- add auth and permissions to views.py
    - import TokenAuthentication from rest framework
    - update viewset class to add tuples specifying desired auth classes, and permission classes

### search functionality
- search for objects
- update views.py file from app
- import filters from rest_framework
- add filters_backend tuple to class w/ searchfilter function
- create search_field tuple to specify the fields that can be used to search

### login functionality
- create a viewset that acts as a login/auth form
- in views.py of app
    - import authtokenserializer
    - import obtain auth token
    - add a class for the loginView
    - create a authtokenserializer 
    - define a create function that returns obtainauthtoken and posts
- in urls.py of app
    - register the login view with the router

### adding a new model
- create the model in the apps model.py file
- create and run migration
    - access server and login to virtual env, cd to project directory
    - python manage.py makemigrations
    - python manage.py migrate
- register to admin page
    - in admin.py for app:
    - admin.site.register("model")
