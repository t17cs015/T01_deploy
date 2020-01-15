from django import forms  # @UnresolvedImport
from .models import Request , Customer

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