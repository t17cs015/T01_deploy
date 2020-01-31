from django import forms  # @UnresolvedImport
from .models import Request , Customer
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email','name','organization_name','tell_number']

class RequestIdForm(forms.Form):
    request_id = forms.IntegerField(label='ID')

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['scheduled_entry_datetime', 'scheduled_exit_datetime', 'purpose_admission']
        # 'scheduled_entry_datetime', 'scheduled_exit_datetime', 

class RequestPasswordForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['password']

class RequestGetForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['scheduled_entry_datetime', 'scheduled_exit_datetime','entry_datetime','exit_datetime', 'purpose_admission',  'email']

class RequestSendForm(forms.Form):
    organization_name = forms.CharField(label = '組織名',max_length=60)
    name = forms.CharField(label = '氏名')
    tell_number_validator = RegexValidator(regex=r'^(\+([0-9]){1,4}-[1-9]([0-9]){1,3}|0([0-9]){1,3})-([0-9]){1,4}-([0-9]){1,4}$', message=("半角数字とハイフンを用いて電話番号を入力してください"))
    tell_number = forms.CharField(max_length = 19, label = '電話番号',validators=[tell_number_validator])
    email = forms.EmailField(label = 'メールアドレス')
    scheduled_entry_datetime = forms.DateTimeField(label = '入館予定日時')
    scheduled_exit_datetime = forms.DateTimeField(label = '退館予定日時')
    purpose_admission = forms.CharField(label = '申請目的',max_length=255)

class AdminLoginForm(AuthenticationForm):
    def __init(self, *args, **kwargs):
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-ontral'
            field.widget.attrs['placeholder'] = field.label

