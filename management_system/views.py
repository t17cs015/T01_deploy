from django.http import HttpResponse
from django.contrib import messages  # メッセージフレームワーク
from django.shortcuts import redirect , render
from django.utils import timezone
from django.urls import path # for send mail
from django.core.mail import BadHeaderError , send_mail

import datetime,pytz,random, string

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .forms import RequestForm
from .models import Request
from . import views

class RequestMainView(TemplateView):
    template_name = 'management_system/request_main.html'


# def index(request):
#     # return HttpResponse("Hello, world. You're at the management_system index.")

# def detail(request, request_id):
#     return HttpResponse("You're looking at request %s." % request_id)

# def results(request, request_id):
#     response = "You're looking at the results of request %s."
#     return HttpResponse(response % request_id)

# def vote(request, request_id):
#     return HttpResponse("You're voting on request %s." % request_id)

class RequestAddView(CreateView):
    model = Request
    # fields = ('scheduled_entry_datetime', 'scheduled_exit_datetime', 'email')
    template_name = 'management_system/request_add.html'
    success_url = '/management_system'
    form_class = RequestForm

    def post(self, request, *args, **kwargs):
        context_object_name = 'sample_create'
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.request_datetime = timezone.localtime()
            obj.password = ''.join([random.choice(string.digits) for i in range(4)])
            obj.save()
            print("Ill send")
            return self.form_valid(form,obj)
        else:
            return self.form_invalid(form)

    def form_valid(self, form,obj):
        # messages.success(self.request, "保存しました")
        print("保存しました")

        subject = 'W DC Center'
        massage = obj.email.name+'さん\n\nW社です\n\nDBセンター利用ご予約を受け取りましたので報告いたします\n\n申請日時 : ' + obj.request_datetime.strftime('%Y/%m/%d %H:%M:%S') + '\n入館予定日時 : '+obj.scheduled_entry_datetime.strftime('%Y/%m/%d %H:%M:%S') +'\n退館予定日時 : '+obj.scheduled_exit_datetime.strftime('%Y/%m/%d %H:%M:%S') +'\n電話番号 : ' + obj.email.tell_number + '\nこれは予約を保証するものではありません\n申請が取り消される場合がございます'
        from_email = 'dbcenterw1@gmail.com'
        recipient_list = [
            obj.email.__str__()
        ]
        # print("send mail")
        send_mail(subject,massage,from_email,recipient_list)
        return super().form_valid(form)

    def form_invalid(self, form):
        # message.warning(self.request, "保存できませんでした")
        print("保存できませんでした")
        return super().form_invalid(form)
