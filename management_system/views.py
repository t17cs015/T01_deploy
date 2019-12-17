from django.http import HttpResponse
from django.contrib import messages  # メッセージフレームワーク
from django.shortcuts import redirect

import datetime,random, string

from django.views.generic.edit import CreateView 
from .forms import RequestForm
from .models import Request

def index(request):

    return HttpResponse("Hello, world. You're at the management_system index.")

def detail(request, request_id):
    return HttpResponse("You're looking at request %s." % request_id)

def results(request, request_id):
    response = "You're looking at the results of request %s."
    return HttpResponse(response % request_id)

def vote(request, request_id):
    return HttpResponse("You're voting on request %s." % request_id)

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
            now = datetime.datetime.now()
            obj.request_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
            obj.password = ''.join([random.choice(string.digits) for i in range(4)])
            obj.save()
            return redirect('/management_system', pk=obj.pk)

    def form_valid(self, form):
        # messages.success(self.request, "保存しました")
        print("保存しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        # message.warning(self.request, "保存できませんでした")
        print("保存できませんでした")
        return super().form_invalid(form)
