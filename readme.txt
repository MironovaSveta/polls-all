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

42. use generic views: less code is better
    detail() and results() views are redunadant, index() view is similar
    these views represent a common case of basic web development:
      * get data from the database according to a parameter passed in the URL
      * load a template
      * return the rendered template
    it is common => a shortcut, called the "generic views" system

    - amend URLconf
      polls/urls.py
    - amend views
      polls/views.py
      use two generic views: ListView ("display a list of objects") and DetailView ("display a detail page for a particular type of object")

    generic view needs: model, primary key of the object

    by default, DetailView uses a template called <all name>/<model name>_detail.html, etc.

##################################################################################
automated testing

43. create a test
    polls.tests.py

44. run tests
    python manage.py test polls

svetlanamironova=# ALTER USER mydatabaseuser CREATEDB;
ALTER ROLE
svetlanamironova-# \q
svetlanamironova@MacBook-Air-Svetlana ~/D/r/d/p/mysite (main)> python manage.py test polls
Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
F
======================================================================
FAIL: test_was_published_recently_with_future_question (polls.tests.QuestionModelTests)
was_published_recently() returns False for questions whose pub_date
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/svetlanamironova/Documents/repo/django-apps/poll-application/mysite/polls/tests.py", line 20, in test_was_published_recently_with_future_question
    self.assertIs(future_question.was_published_recently(), False)
AssertionError: True is not False

----------------------------------------------------------------------
Ran 1 test in 0.009s

FAILED (failures=1)
Destroying test database for alias 'default'...
svetlanamironova@MacBook-Air-Svetlana ~/D/r/d/p/mysite (main) [1]> 

45. fixing the bug
    polls/models.py

46. run tests again

svetlanamironova@MacBook-Air-Svetlana ~/D/r/d/p/mysite (main) [1]> python manage.py test polls
Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.003s

OK
Destroying test database for alias 'default'...

47. Django test client
    python manage.py shell
    from django.test.utils import setup_test_environment
    setup_test_environment()
      installs a template renderer, does not set up a test database
    from django.test import Client
    client = Client()

    response = client.get("/")
      Not Found: /
    response.status_code
      404

    from django.urls import reverse
    response = client.get(reverse("polls:index"))
    response.status_code
      200
    response.content
      b'\n    <ul>\n    \n        <li><a href="/polls/1/">What&#x27;s up?</a></li>\n    \n    </ul>\n'
    response.context["latest_question_list"]
      <QuerySet [<Question: What's up?>]>

48. a test for a view
    polls/tests.py, in class QuestionIndexViewTests -- test index view
                  , in class QuestionDetailViewTests -- test detail view

Good rules-of-thumb include having:
  * a separate TestClass for each model or view
  * a separate test method for each set of conditions you want to test
  * test method names that describe their function

##########################################################################################################
static files

static files -- images, JavaScript, CSS
  necessary to render the complete web page

django.contrib.staticfiles collects static files from each of your applications into a single location

49. polls/static/polls/style.css

50. add previous path to polls/templates/polls/index.html

##########################################################################################################
customize the admin form

51. polls/admin.py
    * reorder the fields
    * split the fields into fieldsets

52. add related objects
    two ways: register Choice / add a bunch of Choices directly when create the Question model

53. customize the admin change list
    include the was_published_recently() method

54. configure the was_published_recently() method via the decorator

55. add filter

56. customize project's templates
    add DIRS to mysite/mysite/settings.py
    DIRS -- a list of filesystem directories to check when loading Django templates

    find Django source files
      python -c "import django; print(django.__path__)"
    
    copy admin/base_site.html from Django source files (django/contrib/admin/templates) to polls/templates/admin/base_site.html

    change site_header in polls/templates/admin/base_site.html

    it is approach how to override templates

##########################################################################################################
third-party packages

57. install django debug toolbar
    python -m pip install django-debug-toolbar

58. Get help at Django forum, join the Django Discord server