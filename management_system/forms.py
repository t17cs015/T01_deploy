from django import forms  # @UnresolvedImport
from .models import Request

# class ItemBuy(forms.Form):
#     status = (
#         (0, "未購入"),
#         (1, "購入済")
#         )
#     item_id = forms.IntegerField(label = "ID")
#     item_status = forms.ChoiceField(label = "STATUS", widget = forms.Select, choices = status)
  
# class ItemIdForm(forms.Form):
#     item_id = forms.IntegerField(label='ID')

# class ItemForm(forms.ModelForm):
#     class Meta:
#         model = Item
#         fields = ['name', 'item_url', 'count', 'buy_date', 'shop'] 


# class CustomerForm(forms.Form):
#     email = forms.EmailField()
#     name = forms.CharField(max_length=60)
#     organization_name = forms.CharField(max_length=60)
#     tell_number = forms.CharField(max_length=15)


class RequestForm(forms.Form):
    # scheduled_entry_datetime = forms.DateTimeField()
    # scheduled_exit_datetime = forms.DateTimeField()
    # entry_datetime = forms.DateTimeField()
    # exit_datetime = forms.DateTimeField()
    # purpose_admission = forms.CharField(max_length=255)
    # request_datetime = forms.DateTimeField()
    # email = forms.ForeignKey(Customer)
    # # 通し番号はID
    # approval = forms.IntegerField(default=0)
    # password = forms.IntegerField(default=0)

    class Meta:
        model = Request
        fields = ['scheduled_entry_datetime', 'scheduled_exit_datetime', 'purpose_admission', 'request_datetime', 'email']

