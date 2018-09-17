Environize
========================================

.. image:: https://travis-ci.org/cgdeboer/environize.svg?branch=master
    :target: https://travis-ci.org/cgdeboer/environize

.. image:: https://img.shields.io/pypi/v/iteround.svg
    :target: https://pypi.org/project/environize/

.. image:: https://raw.githubusercontent.com/cgdeboer/environize/master/docs/environize.png

**Environize enables environment and state savvy DataMigration tools for Django**

1. Decorators
    - adds a pair of decorators (**only_in** and **except_in**) for use with the **migrations.RunPython** method.
    - use django's DataMigrations to allow dev data and prod data to be different.
    - exclude large data creation migrations from tests which may define their own data.

2. Command(s)
    - adds a **loaddata** method that loads JSON fixtures into the database based on the state of the migration.
    - different from ``./manage.py loaddata`` or ``call_command("loaddata")``, which both load fixtures to the database based on the current state of models.
    - no more updating fixtures to keep them current. The data model in the fixture is tied to the state of your models in the migration.

Decorators - Usage
------------------

*Exclude Tests*

.. code-block:: python

    from django.db import migrations
    import environize

    # runs in every env except testing
    @environize.except_in(envs=["test"])
    def except_test_data(apps, schema_editor):
        Ham = apps.get_model("app", "Ham")
        Ham.objects.create(name="not-test")

    @environize.except_in(envs=["test"])
    def remove_hams(apps, schema_editor):
        Ham = apps.get_model("app", "Ham")
        Ham.objects.all().delete()


    class Migration(migrations.Migration):

        dependencies = [
            ('app', '0002_auto_20180916_1122'),
        ]

        operations = [
            migrations.RunPython(except_test_data, remove_hams)
        ]

*Production Only Data*

.. code-block:: python

    from django.db import migrations
    import environize

    # runs in every env except testing
    @environize.only_in(envs=["production"])
    def add_prod_data(apps, schema_editor):
        Ham = apps.get_model("app", "Ham")
        Ham.objects.create(name="not-test")

    @environize.only_in(envs=["production"])
    def remove_hams(apps, schema_editor):
        Ham = apps.get_model("app", "Ham")
        Ham.objects.all().delete()


    class Migration(migrations.Migration):

        dependencies = [
            ('app', '0002_auto_20180916_1122'),
        ]

        operations = [
            migrations.RunPython(add_prod_data, remove_hams)
        ]


Commands - Usage
------------------

.. code-block:: python

    import os
    from django.db import migrations
    import environize

    PATH = 'path/to/fixtures/'

    def load_fixture(apps, schema_editor):
        fixture_file = os.path.join(PATH, 'myfixture.json')
        environize.loaddata(apps, fixture_file)


    class Migration(migrations.Migration):

        dependencies = [
            ('app', '0003_auto_20180916_1122'),
        ]

        operations = [
            migrations.RunPython(load_fixture, lambda x, y: None)
        ]



Feature Support
---------------

Environize officially supports:
    - Python 2.7 on Django 1.11 LTS
    - Python 3.5+ on Django 2+


Installation
------------

To install Environize, use `pipenv <http://pipenv.org/>`_ (or pip, of course):

.. code-block:: bash

    $ pipenv install environize


*Inside various settings files set an ENVIRONMENT variable.*

.. code-block:: python

    # /settings_production.py
    ENVIRONMENT = 'production'

    # /settings_qa.py
    ENVIRONMENT = 'qa'

    # /settings_dev.py
    ENVIRONMENT = 'dev'

The default env keys are listed below but can be overridden by setting ENVIRONIZE_ENVS in your django settings:

.. code-block:: python

    # these are the default env keys
    ENVIRONIZE_ENVS = ("dev", "test", "ci", "qa", "staging", "production")

    # by default this key will be used if one is not set in a settings file.
    DEFAULT_ENV = "dev"


Documentation
-------------

TBD


How to Contribute
-----------------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request. Make sure to add yourself to AUTHORS_.

.. _`the repository`: https://github.com/cgdeboer/environize
.. _AUTHORS: https://github.com/cgdeboer/environize/blob/master/AUTHORS.rst
