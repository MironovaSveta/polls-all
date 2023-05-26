Let's write a basic poll application based on Django Documentation tutorial

1. Check if Django is installed already
   $ python3 -m django --version

2. Virtual environment:
   $ python3 -m venv myvenv
   $ source myvenv/bin/activate

3. Install Django
   (myvenv) $ pip install -r requirements.txt

4. Create a project
   (myvenv) $ django-admin startproject mysite

   Creates:
   mysite/ root directory is a container for my project, I can rename it
   manage.py -- a command-line utility that lets me interact with the Django project
   inner mysite/ -- actual Python package for my project

5. Run the development server
   (myvenv) $ python3 manage.py runserver

#######################################################################################
Create app

6. Create app
   An app is a web application that does something
   A project is a collection of configuration and apps for a particular website
   A project can contain multiple apps
   An app can be in multiple projects

   go to the same directory as manage.py and run:
   (myvenv) $ python3 manage.py startapp polls

   that'll create a directory polls/

7. Write the first view
   in polls/views.py add index(request) function
   to call the view, we need to map it to a URL -- so use URLconf
   
8. Create a URLconf in the polls directory
   create file polls/urls.py

9. Point the root URLconf to the polls.urls module
   modify mysite/urls.py