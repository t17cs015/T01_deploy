import datetime

from django import forms
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Customer(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=60)
    organization_name = models.CharField(max_length=60)
    tell_number_validator = RegexValidator(regex=r'^(\+([0-9]){1,4}-[1-9]([0-9]){1,3}|0([0-9]){1,3})-([0-9]){1,4}-([0-9]){1,4}$', message=("半角数字とハイフンを用いて電話番号を入力してください"))
    tell_number = models.CharField(validators=[tell_number_validator], max_length = 19, verbose_name = '電話番号', blank=False)

    def __str__(self):
        return str(self.email)


class Request(models.Model):
    scheduled_entry_datetime = models.DateTimeField('date published',blank = False,null=False)
    scheduled_exit_datetime = models.DateTimeField('date published',blank = False,null=False)
    entry_datetime = models.DateTimeField('date published', blank = True,null = True)
    exit_datetime = models.DateTimeField('date published' , blank = True,null = True)
    purpose_admission = models.CharField(max_length=255)
    request_datetime = models.DateTimeField('date published' ,blank = True,null = True)
    email = models.ForeignKey(Customer, on_delete=models.CASCADE)
    approval = models.IntegerField(default=0)
    password = models.IntegerField(default=None)

    def __str__(self):
        return "{} ({})".format(self.pk , self.email)
