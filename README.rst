=============================
django-consul-cache
=============================

.. image:: https://badge.fury.io/py/django-consul-cache.svg
    :target: https://badge.fury.io/py/django-consul-cache

.. image:: https://travis-ci.org/thanos/django-consul-cache.svg?branch=master
    :target: https://travis-ci.org/thanos/django-consul-cache

.. image:: https://codecov.io/gh/thanos/django-consul-cache/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/thanos/django-consul-cache

A Consul based django cache

Documentation
-------------

The full documentation is at https://django-consul-cache.readthedocs.io.

Quickstart
----------

Install django-consul-cache::

    pip install django-consul-cache

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_consul_cache.apps.DjangoConsulCacheConfig',
        ...
    )

Add django-consul-cache's URL patterns:

.. code-block:: python

    from django_consul_cache import urls as django_consul_cache_urls


    urlpatterns = [
        ...
        url(r'^', include(django_consul_cache_urls)),
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
