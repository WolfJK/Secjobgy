from __future__ import absolute_import
from django.http.response import JsonResponse
from django.contrib.auth import login as auth_login, authenticate
from django.core.paginator import Paginator
from .models import *
from utils.redis_util import cache
from utils.args_util import post_arg_parse
from celery import shared_task, current_app
import uuid


def login(request):
    args = post_arg_parse(request)
    user_name = args.get("user_name", "")
    password = args.get("password", "")
    user = authenticate(username=user_name, password=password)
    if not user:
        return JsonResponse(dict(msg="密码不对"), status=400)
    auth_login(request, user)
    token = str(uuid.uuid4())
    cache.set(name=token, value=token, ex=3600)

    return JsonResponse(dict(token=token))


def search(request):
    args = post_arg_parse(request)
    empno = args.get("empno")
    size = args.get("size", 5)
    num = args.get("num", 1)
    page = Paginator(Employee.objects.filter(empno__in=empno).values("empno", "name", "group__name"), size)
    data = page.get_page(num)
    return JsonResponse(dict(msg="成功", data=list(data), total=page.count))


def new_emp(request):
    task = new_emp_task.delay(post_arg_parse(request))
    return JsonResponse(dict(msg="任务已提交", data=dict(task_id=task.id, task_status=task.status)))


def new_tmp_status(request):
    args = post_arg_parse(request)
    task_id = args.get("task_id")
    task = current_app.AsyncResult(task_id)
    data = dict(task_status=task.status, task_id=task_id)

    data["results"] = task.get()

    return JsonResponse(data)


@shared_task
def new_emp_task(args):
    try:
        org = Organization.objects.filter(pk__in=args.get("org"))
        emp = Employee(
            name=args.get("name"),
            empno=args.get("empno"),
        )
        emp.save()
        emp.group.add(*org)
    except Exception as e:
        print(e)



def new_org(request):
    args = post_arg_parse(request)
    org = Organization(
        name=args.get("name"),
        type=args.get("type"),
    )
    org.save()
    return JsonResponse(dict(msg="创建成功"))


