# coding: utf-8
# __author__: u"John"
from __future__ import unicode_literals, print_function
from django.core.exceptions import ValidationError
from django.db import models
import uuid


class Organization(models.Model):
    type_choice = (
        (1, "开发"),
        (2, "运维"),
        (3, "产品"),
        (4, "测试")
    )
    name = models.CharField(max_length=50, unique=True, db_index=True)
    type = models.IntegerField(choices=type_choice)

    class Meta:
        db_table = "org"


class Employee(models.Model):
    uuid = models.CharField(primary_key=True, max_length=36, default=str(uuid.uuid4()))
    name = models.CharField(blank=False, null=False, max_length=32)
    empno = models.BigIntegerField(blank=False, null=False, db_index=True, unique=True)
    group = models.ManyToManyField(Organization)

    class Meta:
        db_table = "emp"

    def clean(self):
        if self.empno > 50000:
            raise ValidationError("empno不能大于50000")
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
