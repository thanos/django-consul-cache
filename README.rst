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

AModify your Django settings to use `django_consul_cache`:

.. code-block:: python

    CACHES = {
        'default': {
            'BACKEND': 'django_consul_cache.ConsulCache',
            'LOCATION': 'localhost:8500',
        },
    }

django-redis-cache shares the same API as django's built-in cache backends

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
