=====
Usage
=====

To use django-consul-cache in a project, add it to your `INSTALLED_APPS`:

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
