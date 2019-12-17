import datetime

from django.db import models
from django.utils import timezone


class Customer(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=60)
    organization_name = models.CharField(max_length=60)
    tell_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Request(models.Model):
    scheduled_entry_datetime = models.DateTimeField('date published')
    scheduled_exit_datetime = models.DateTimeField('date published')
    entry_datetime = models.DateTimeField('date published', blank = True,null = True)
    exit_datetime = models.DateTimeField('date published' , blank = True,null = True)
    purpose_admission = models.CharField(max_length=255)
    request_datetime = models.DateTimeField('date published')
    email = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 通し番号はID
    approval = models.IntegerField(default=0)
    password = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)