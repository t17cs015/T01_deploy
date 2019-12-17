import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Customer(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=60)
    organization_name = models.CharField(max_length=60)
    tell_number_validator = RegexValidator(regex=r'^(\+([0-9]){1,4}-[1-9]([0-9]){1,3}|0([0-9]){1,3})-([0-9]){1,4}-([0-9]){1,4}$', message=("半角数字とハイフンを用いて電話番号を入力してください"))
    tell_number = models.CharField(validators=[tell_number_validator], max_length = 114514, verbose_name = '電話番号', blank=False)

    def __str__(self):
        return self.name

class Request(models.Model):
    scheduled_entry_datetime = models.DateTimeField('date published')
    scheduled_exit_datetime = models.DateTimeField('date published')
    entry_datetime = models.DateTimeField('date published')
    exit_datetime = models.DateTimeField('date published')
    purpose_admission = models.CharField(max_length=255)
    request_datetime = models.DateTimeField('date published')
    email = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # 通し番号はID
    approval = models.IntegerField(default=0)
    password = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)
