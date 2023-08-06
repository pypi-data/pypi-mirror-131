django-popups
==========

django-popups is a Django app to use for demiansoft. For each question,
visitors can choose between a fixed number of answers.

Quick start
------------

1. Add "popups" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'popups',
    ]

2. Run below command to create the popups models.::

    python manage.py makemigrations popups
    python manage.py migrate

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a popups (you'll need the Admin app enabled).

4. In the view.py, add a following code for making a popup context::

    from popups.views import make_popups_context
    ...
    # in the index function..
    context = make_popups_context()

5. For show the popup on the web page, add the following code in html like this::

    {% include 'popups/show.html' %}
