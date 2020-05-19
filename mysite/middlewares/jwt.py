# coding: utf-8
# __author__: u"John"
from __future__ import unicode_literals, print_function
from django.http import JsonResponse
from utils.redis_util import cache
from utils.args_util import post_arg_parse
from datetime import datetime

jwt_skip_set = {"/api/login"}


def jwt_middleware(get_response):
    def middleware(request):
        now = datetime.now()
        method = request.method
        user = request.user
        path = request.path
        args = post_arg_parse(request)
        ip = request.META.get("REMOTE_ADDR")
        log = f"{now} {method} {path} {user} {ip} {args}\n"

        with open("log", "a+") as f:
            f.write(log)

        if request.path not in jwt_skip_set:
            token = request.META.get("HTTP_TOKEN")
            not_login_response = JsonResponse(dict(msg="请先登陆"), status=400)

            if token is None:
                return not_login_response

            if cache.get(token) is None:
                return not_login_response

            cache.set(name=token, value=token, ex=3600)
        return get_response(request)

    return middleware
