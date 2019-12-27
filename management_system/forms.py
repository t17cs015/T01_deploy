from django import forms  # @UnresolvedImport
from .models import Request , Customer
from django.contrib.auth.forms import AuthenticationForm

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email','name','organization_name','tell_number']

class RequestIdForm(forms.Form):
    request_id = forms.IntegerField(label='ID')

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['scheduled_entry_datetime', 'scheduled_exit_datetime', 'purpose_admission',  'email']

class RequestPasswordForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['password']

class RequestGetForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['scheduled_entry_datetime', 'scheduled_exit_datetime','entry_datetime','exit_datetime', 'purpose_admission',  'email']

class AdminLoginForm(AuthenticationForm):
    def __init(self, *args, **kwargs):
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-ontral'
            field.widget.attrs['placeholder'] = field.label


