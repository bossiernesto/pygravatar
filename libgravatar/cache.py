import datetime,collections
import functools

CACHE_DURATION=30

def Cache(ttl=CACHE_DURATION):
    class _Cache(object):
        """Cache Decorator. Caches a function's return value each time it is called.
        If called later with the same arguments, the cached value is returned
        (not reevaluated) unless the ttl expires (default 30 mins).
        arguments:  ttl (in minutes)
        """
        def __init__(self, func):
            self.func = func
            self.cache = {}
            self.timestamp={}
            self.method_cache = {}
            self.method_timestamp={}
            self.duration=ttl

        def __call__(self, *args):
            return self.cache_get(self.cache, args,
                lambda: self.func(*args),self.timestamp)

        def __get__(self, obj, objtype):
            return self.cache_get(self.method_cache, obj,
                lambda: self.__class__(functools.partial(self.func, obj)),self.method_timestamp)

        def cache_get(self, cache, key, func,timestamp):
            if not isinstance(key, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
                return self.func()
            try:
                if self.hasExpired(timestamp[key]):
                    cache.pop(key)
                return cache[key]
            except KeyError:
                cache[key] = func()
                timestamp[key]=self.getExpireTime()
                return cache[key]

        def getExpireTime(self):
            return self.addMins(datetime.datetime.now(),self.duration)

        def hasExpired(self,timestamp):
            return datetime.datetime.now()>=timestamp

        def addMins (self,tm,mins):
            fulldate = datetime.datetime(tm.year,tm.month,tm.day,tm.hour,tm.minute,tm.second)
            fulldate = fulldate + datetime.timedelta(minutes=mins)
            return fulldate

    return _Cache
