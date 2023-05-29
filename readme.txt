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

#######################################################################################
Database setup

10. Switch from default SQLite to PostgreSQL
    in file mysite/mysite/settings.py

11. install Postgres.app
    configure the $PATH variable
    check by typing "which psql"

12. create the database
    12.1 psql
    12.2 CREATE USER mydatabaseuser;                                                                                            
         CREATE DATABASE mydatabase OWNER mydatabaseuser;
    12.3 \q

13. (myvenv) $ python3 manage.py migrate
    looks at the INSTALLED_APPS settings and creates any necessary database tables

#######################################################################################
Create models

14. Edit classes Question, Choice at mysite/polls/models.py

15. add 'polls.apps.PollsConfig' to mysite/mysite/settings.py

16. activate models
    python3 manage.py makemigrations polls

17. see what SQL that migration would run
    python3 manage.py sqlmigrate polls 0001

18. create model tables
    python3 manage.py migrate

######################################################################################
Django API

19. python3 manage.py shell

20. explore the database API

>>> from polls.models import Choice, Question
>>> Question.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()
>>> q.id
1
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2023, 5, 26, 16, 11, 37, 760741, tzinfo=datetime.timezone.utc)
>>> q.question_text = "What's up?"
>>> q.save()
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>

21. add methods to classes Question, Choice
    __str__ -- important to add

######################################################################################
creating an admin user

22. python manage.py createsuperuser
    admin - password

23. start the development server
    python manage.py runserver

24. go to /admin/ on your local domain -- e.g. http://127.0.0.1:8000/

25. enter the admin site
    you should see the Django admin index page

26. make the poll app modifiable in the admin
    change polls/admin.py

#####################################################################################
views

a view is a "type" of web page in Django app that generally serves a specific function and has a specific template
a view is represented by a python function (or method, in the case of class-based views)
a URLconf maps URL patterns to views

E.g. for poll app:
* Question "index" page -- displays the latest few questions
* Question "detail" page -- displays a question text, with no results but with a form to vote
* Question "results" page -- displays results for a particular question
* Vote action -- handles voting for a particular choice in a particular question

each view is responsible for returning HttpResponse object or raising an exception such as Http404

27. write more views
    in polls/views.py

28. add these new views into the polls.urls module
    in polls/urls.py

####################################################################################
templates

29. write views that actually do something
    the page's design is hard-coded in the view, so use Django's template system 

30. create polls/templates/ directory
    creare polls/templates/polls/index.html

31. update view to use the template

32. learn about a shortcut: render()

33. raising a 404 error
    try, except raise Http404

34. learn about a shortcut: get_object_or_404()

35. use the template system

36. remove hardcoded URLs in templates

37. add namespaces to URLconf
    because Django should differentiate between apps

###################################################################################
add form

38. polls/templates/polls/detail.html
    set method = post!
      because the form alters data server-side
    all POST forms that are targeted at internal URLs should use the csrf_token

39. polls/views.py
    returns an HttpResponseRedirect instead of HttpResponse
      it is a good practice after successfully dealing with POST data
    !!! a small problem: a race condition. appears when two users try to vote at the same time
        because a new value of votes computes and saves it back to the database

40. polls/templates/polls/results.html

41. add choices
>>> from polls.models import Choice, Question
>>> q = Question.objects.get(pk=1)
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: Not much>]>
>>> q.choice_set.create(choice_text="The sky", votes=0)
<Choice: The sky>
>>> q.choice_set.create(choice_text="Just hacking", votes=0)
<Choice: Just hacking>
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: Not much>, <Choice: The sky>, <Choice: Just hacking>]>
>>> q.ch
q.check(      q.choice_set(
>>> q.choice_set[1]
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: 'RelatedManager' object is not subscriptable
>>> q.choice_set.filter(id=1).delete()
(1, {'polls.Choice': 1})
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking>]>
