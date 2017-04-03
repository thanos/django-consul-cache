# -*- coding: utf-8 -*-
# Author:
#  Thanos Vassilakis <thanosvatgmail.com>, (c) 2017
#
# based on https://github.com/Alir3z4/django-mongodb-cash-backend/blob/master/django_mongodb_cash_backend/__init__.py

__version__ = '0.1.0'
try:
    import cPickle as pickle
except ImportError:
    import pickle
import base64
import re
from datetime import datetime, timedelta
import consulate

from django.core.cache.backends.base import BaseCache


class ConsulCache(BaseCache):
    def __init__(self, location, params):
        super(ConsulCache, self).__init__(params)
        self.location = location
        options = params.get('OPTIONS', {})
        self._host = options.get('HOST', 'localhost')
        self._port = options.get('PORT', 27017)
        self.root = options.get('/DJANGO-CACHE/')
        self.session = consulate.Consul()

    def make_key(self, key, version=None):
        """
         Additional regexp to remove $ and . cachaters,
        as they cause special behaviour in Consul
        """
        key = super(ConsulCache, self).make_key(key, version)

        return re.sub(r'\$|\.', '', key)

    def add(self, key, value, timeout=None, version=None):
    	"""
        Set a value in the cache if the key does not already exist. If
        timeout is given, use that timeout for the key; otherwise use the
        default cache timeout.
        Return True if the value was stored, False otherwise.
		"""
		key = self.make_key(key, version)
        self.validate_key(key)
        if key in session:
        	return False
        session[key] = value 
        return True

    def get(self, key, default=None, version=None):
        """
        Fetch a given key from the cache. If the key does not exist, return
        default, which itself defaults to None.
        """
		try:
		    should_release_feature = session.kv['release_flag']
		except AttributeError:
		    return default

    def set(self, key, value, timeout=None, version=None):
        key = self.make_key(key, version)
        self.validate_key(key)
        return self._base_set('set', key, value, timeout)

    def delete(self, key, version=None):
        """
        Delete a key from the cache, failing silently.
        """
        raise NotImplementedError('subclasses of BaseCache must provide a delete() method')

    def get_many(self, keys, version=None):
        """
        Fetch a bunch of keys from the cache. For certain backends (memcached,
        pgsql) this can be *much* faster when fetching multiple values.
        Return a dict mapping each key in keys to its value. If the given
        key is missing, it will be missing from the response dict.
        """
        d = {}
        for k in keys:
            val = self.get(k, version=version)
            if val is not None:
                d[k] = val
        return d

    def get_or_set(self, key, default, timeout=DEFAULT_TIMEOUT, version=None):
        """
        Fetch a given key from the cache. If the key does not exist,
        add the key and set it to the default value. The default value can
        also be any callable. If timeout is given, use that timeout for the
        key; otherwise use the default cache timeout.
        Return the value of the key stored or retrieved.
        """
        val = self.get(key, version=version)
        if val is None and default is not None:
            if callable(default):
                default = default()
            self.add(key, default, timeout=timeout, version=version)
            # Fetch the value again to avoid a race condition if another caller
            # added a value between the first get() and the add() above.
            return self.get(key, default, version=version)
        return val

    def has_key(self, key, version=None):
        """
        Return True if the key is in the cache and has not expired.
        """
        return self.get(key, version=version) is not None

    def incr(self, key, delta=1, version=None):
        """
        Add delta to value in the cache. If the key does not exist, raise a
        ValueError exception.
        """
        value = self.get(key, version=version)
        if value is None:
            raise ValueError("Key '%s' not found" % key)
        new_value = value + delta
        self.set(key, new_value, version=version)
        return new_value

    def decr(self, key, delta=1, version=None):
        """
        Subtract delta from value in the cache. If the key does not exist, raise
        a ValueError exception.
        """
        return self.incr(key, -delta, version=version)

    def __contains__(self, key):
        """
        Return True if the key is in the cache and has not expired.
        """
        # This is a separate method, rather than just a copy of has_key(),
        # so that it always has the same functionality as has_key(), even
        # if a subclass overrides it.
        return self.has_key(key)

    def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None):
        """
        Set a bunch of values in the cache at once from a dict of key/value
        pairs.  For certain backends (memcached), this is much more efficient
        than calling set() multiple times.
        If timeout is given, use that timeout for the key; otherwise use the
        default cache timeout.
        """
        for key, value in data.items():
            self.set(key, value, timeout=timeout, version=version)

    def delete_many(self, keys, version=None):
        """
        Delete a bunch of values in the cache at once. For certain backends
        (memcached), this is much more efficient than calling delete() multiple
        times.
        """
        for key in keys:
            self.delete(key, version=version)

    def clear(self):
        """Remove *all* values from the cache at once."""
        raise NotImplementedError('subclasses of BaseCache must provide a clear() method')

    def validate_key(self, key):
        """
        Warn about keys that would not be portable to the memcached
        backend. This encourages (but does not force) writing backend-portable
        cache code.
        """
        if len(key) > MEMCACHE_MAX_KEY_LENGTH:
            warnings.warn(
                'Cache key will cause errors if used with memcached: %r '
                '(longer than %s)' % (key, MEMCACHE_MAX_KEY_LENGTH), CacheKeyWarning
            )
        for char in key:
            if ord(char) < 33 or ord(char) == 127:
                warnings.warn(
                    'Cache key contains characters that will cause errors if '
                    'used with memcached: %r' % key, CacheKeyWarning
                )
                break

    def incr_version(self, key, delta=1, version=None):
        """
        Add delta to the cache version for the supplied key. Return the new
        version.
        """
        if version is None:
            version = self.version

        value = self.get(key, version=version)
        if value is None:
            raise ValueError("Key '%s' not found" % key)

        self.set(key, value, version=version + delta)
        self.delete(key, version=version)
        return version + delta

    def decr_version(self, key, delta=1, version=None):
        """
        Subtract delta from the cache version for the supplied key. Return the
        new version.
        """
        return self.incr_version(key, -delta, version)

    def close(self, **kwargs):
        """Close the cache connection"""
        pass