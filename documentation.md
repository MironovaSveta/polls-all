# Polls Website Technical Documentation

## Project Structure

```markdown
- mysite/
  - polls/
    - migrations/
    - static/
      - polls/
    - templates/
      - admin/
      - polls/
  - templates/
  - manage.py
- myvenv/
  - bin/
  - include/
  - lib/
```

## URLs

* Index page (List of Questions): /polls/
* Detail page (Question and Choices): /polls/{question_id}/
* Results page (Question Results): /polls/{question_id}/results/
* Vote action (Handle Voting): /polls/{question_id}/vote/
* Admin page: /admin/

## Database Configuration

Database Name: mydatabase

Database User: mydatabaseuser

## Django Debug Toolbar

The Django Debug Toolbar is integrated into your website.
It was installed via pip.
To enable the toolbar, make sure INTERNAL_IPS is set to "127.0.0.1" in your Django settings.
The toolbar will be visible when DEBUG is set to True in your Django settings.
The following line is added to your urls.py file to include the toolbar URLs:

```python
urlpatterns += path('__debug__/', include(debug_toolbar.urls))
```

## Generic Views

ListView and DetailView are implemented for the detail and results pages.
These generic views provide functionality to display a list of questions and show details of a specific question.

## Automated Testing

Automated testing is implemented for your website with 10 tests.
A test database is created to isolate the tests from the production database.
The test client is used to simulate requests and test the website's functionality.

## Additional Notes

The website is designed for polls, where authorized users can create and edit questions, and all users can view and vote on the polls.
The website targets teenagers and adults.
The main page (/polls/) displays a list of questions.
Each question on the main page has a link to its detail page (/polls/{question_id}/), which shows the question text and its choices.
The detail page includes a form to vote on a specific choice for that question (/polls/{question_id}/vote/).
After voting, users can view the results for that question (/polls/{question_id}/results/).
The admin page (/admin/) provides a form to create questions and corresponding choices, along with options for publication date and filtering by publication date.
