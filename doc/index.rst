.. anishare documentation master file, created by
   sphinx-quickstart on Tue May 29 13:02:59 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to anishare's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Webservice to share animals to minimize animal usage

This django app is meant to be used by research institutes that want to share research animals. 
By sharing animals within the institute, less animals in total have to be sacrificed for research.


Installation
------------

Requirements
^^^^^^^^^^^^
We use the latest version of django, which requires python3.
Install django and other dependancies (We recommend using a virtual environment for this)::

    virtualenv -p python3 .
    source bin/activate
    pip install -r requirements.txt
    pip install -r requirements.txt

First time setup
^^^^^^^^^^^^^^^^
Run migrations::

    python manage.py migrate

This will create the sqlite database ``db.sqlite3``.
Now create a superuser::

    python manage.py createsuperuser

You are now able to login to the admin interface, but first run the dev server::

    python manage.py runserver

This will listen on ``http://localhost:8000``, so browse to the admin page 
``http://localhost:8000/admin`` and you should see this after login:

.. image:: img/admin_empty.png


After adding several animals, the main (index) view should look like this:

.. image:: img/anishare_index_view.png

Alternatively, you can also import a dummy set of data using the ``loaddata`` command::

   python manage.py loaddata initial_data.json

.. .. literalinclude:: ../animals/admin.py
..    :language: python
..    :linenos:
..   :lines: 15-28
..   :emphasize-lines: 12,15-18




API documentation
==================

.. include::   modules/models.rst
.. include::   modules/views.rst

.. Indices and tables
.. ==================
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
