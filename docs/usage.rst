=====
Usage
=====

To use Django Ethereum in a project, add it to your `INSTALLED_APPS`:

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
