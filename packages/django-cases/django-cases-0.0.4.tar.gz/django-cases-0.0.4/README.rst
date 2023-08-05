django-cases
==========

django-cases is a Django app to use for demiansoft. For each question,
visitors can choose between a fixed number of answers.

Quick start
------------

1. Add "cases" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'cases',
    ]

2. Run below command to create the cases models.::

    python manage.py makemigrations cases
    python manage.py migrate

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a cases (you'll need the Admin app enabled).

4. In the view.py, add a following code for making a cases and case_detail context::

    from cases.views import make_cases_context
    ...
    # in the index function..
    context = make_cases_context()

5. In the cases web page, link to cases_details page like this::

    {% url 'cases:case_details' id app_name %}

