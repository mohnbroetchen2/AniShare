 Installation
------------

 Requirements
^^^^^^^^^^^^

We use the latest version of `django <https://www.djangoproject.com>`_, which requires `python3 <https://www.python.org>`_. 
Install django and other dependancies (see file requirements.txt. We recommend using a virtual environment for this)::
    virtualenv -p python3 .
    source bin/activate
    pip install -r requirements.txt
First time setup
^^^^^^^^^^^^^^^^

First, in the folder ``anishare``, copy the file ``local_settings.py.template``
to ``local_settings.py`` and fill it in. If you want to use LDAP, comment in
the respective lines. Most importantly, you should configure the following lines::
    EMAIL_HOST = ''
    SECRET_KEY = ''
    ALLOWED_HOSTS = ['127.0.0.1', ]
Then, you can run migrations::
    python manage.py migrate

 note:: This will create the sqlite database ``db.sqlite3`` containing all the models 
          (eg. tables) as defined in :py:mod:`animals.models`.
Now create a superuser::
    python manage.py createsuperuser
You are now able to login to the admin interface, but first run the dev server::
    python manage.py runserver
This will listen on ``http://localhost:8000``, so browse to the admin page 
``http://localhost:8000/admin`` and you should see this after login:

 image:: img/admin_empty.png

You can also import a dummy set of data using the ``loaddata`` command::
   python manage.py loaddata initial_data.json
After loading the data, the main admin interface should look like this:

 image:: img/admin_after_loaddata.png

Importing existing data
^^^^^^^^^^^^^^^^^^^^^^^
For import of existing data in tabular (excel) format, a management command is available at 
:py:mod:`animals.management.commands.import_animals` ::  
   python manage.py import_animals

 Note:: See the file ``example_import.xls`` for an example...
 image:: img/import_excel_sheet.pn

In-DB Caching
^^^^^^^^^^^^^

By default, database caching is enabled in settings. To create the necessary tables, run this
command::
   python manage.py createcachetable
This will create a cache table in the SQLite database, which will speed up queries.

Running Tests
^^^^^^^^^^^^^

Tests reside in ``animals/tests.py``.
You can invoke the django tests like so::
    python manage.py test
   literalinclude:: ../animals/tests.py
   :language: python
   :linenos:

Upgrading django
""""""""""""""""

To upgrade django or any other python library for anishare, go into the anishare directory, and
activate its virtualenv::
   cd anishare
   source bin/activate
Next, install/upgrade whatever library (here: django to the latest version)::
   pip install --upgrade django

 Note:: It's best to test the latest version in a local/development environment first!

Upgrading python
""""""""""""""""
When upgrading the python version of the host operating system, it might be necessary to also
upgrade the python in the virtualenv. Otherwise an error like the following might occur:
   ``python: error while loading shared libraries: libpython3.4m.so.1.0: cannot open shared object file: No such file or directory``
In that case, go into the anishare directory, and delete the following directories:
- bin
- include
- lib
- lib64
Afterwards, create a new virtualenv and install the required libraries like so::
    virtualenv -p python3 .
    source bin/activate
    pip install -r requirements.txt
API documentation
==================
.. include::   modules/admin.rst
.. include::   modules/models.rst
.. include::   modules/views.rst
.. include::   modules/urls.rst