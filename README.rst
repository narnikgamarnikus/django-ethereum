=============================
Django Ethereum
=============================

.. image:: https://badge.fury.io/py/django-ethereum.svg
    :target: https://badge.fury.io/py/django-ethereum

.. image:: https://travis-ci.org/narnikgamarnikus/django-ethereum.svg?branch=master
    :target: https://travis-ci.org/narnikgamarnikus/django-ethereum

.. image:: https://codecov.io/gh/narnikgamarnikus/django-ethereum/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/narnikgamarnikus/django-ethereum

Django using web3.py and etherscan for working with Ethereum

Documentation
-------------

The full documentation is at https://django-ethereum.readthedocs.io.

Quickstart
----------

Install Django Ethereum::

    pip install django-ethereum

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_ethereum.apps.EthereumConfig',
        ...
    )

Add Django Ethereum's URL patterns:

.. code-block:: python

    from django_ethereum import urls as django_ethereum_urls


    urlpatterns = [
        ...
        url(r'^', include(django_ethereum_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
