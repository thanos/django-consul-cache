# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from django_consul_cache.urls import urlpatterns as django_consul_cache_urls

urlpatterns = [
    url(r'^', include(django_consul_cache_urls, namespace='django_consul_cache')),
]
