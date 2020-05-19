# coding: utf-8
# __author__: u"John"
from __future__ import unicode_literals, print_function
import json


def post_arg_parse(request):
    return json.loads(request.body) if request.body else dict()
