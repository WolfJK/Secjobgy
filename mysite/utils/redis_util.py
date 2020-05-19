# coding: utf-8
# __author__: u"John"
from __future__ import unicode_literals, print_function
import redis


class Redis(redis.Redis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = None

    def get(self, *args, **kwargs):
        self.connect()
        return self.connection.get(*args, **kwargs)

    def set(self, *args, **kwargs):
        self.connect()
        self.connection.set(*args, **kwargs)

    def connect(self):
        if self.connection is None:
            self.connection = redis.Redis(host="localhost", port=6379, db=1)

    def close(self):
        self.connection.close()


cache = Redis()
