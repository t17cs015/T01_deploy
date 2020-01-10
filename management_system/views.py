from django.contrib import messages  # メッセージフレームワーク
from django.http import HttpResponseRedirect
from django.shortcuts import redirect , get_object_or_404 , render
from django.utils import timezone
from django.urls import reverse

import datetime,pytz,random, string

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView , UpdateView
from .forms import RequestForm , RequestIdForm , RequestPasswordForm , RequestGetForm
from .forms import CustomerForm

from .models import Request , Customer

class RequestMainView(TemplateView):
    template_name = 'management_system/request_main.html'


# def index(request):
#     # return HttpResponse('Hello, world. You're at the management_system index.')

# def detail(request, request_id):
#     return HttpResponse('You're looking at request %s.' % request_id)

# def results(request, request_id):
#     response = 'You're looking at the results of request %s.'
#     return HttpResponse(response % request_id)

# def vote(request, request_id):
#     return HttpResponse('You're voting on request %s.' % request_id)

class RequestAddView(CreateView):
    model = Request
    # fields = ('scheduled_entry_datetime', 'scheduled_exit_datetime', 'email')
    template_name = 'management_system/request_add.html'
    success_url = '/management_system/main'
    form_class = RequestForm

    def post(self, request, *args, **kwargs):
        # context_object_name = 'sample_create'
        form = self.form_class(request.POST)
        # print(form)
        if form.is_valid():
            obj = form.save(commit=False)
            # now = datetime.datetime.now(pytz.timezone('UTC'))
            # obj.request_datetime = now.astimezone().strftime('%Y-%m-%d %H:%M:%S')
            obj.request_datetime = timezone.localtime()
            obj.password = ''.join([random.choice(string.digits) for i in range(4)])
            obj.save()
            print('save')
            obj.request_id = obj.id
            print('dainyuu')
            obj.save()
            
            print(obj.id)
            print(obj.request_id)
            print('Ill send')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # messages.success(self.request, '保存しました')
        print('保存しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        # message.warning(self.request, '保存できませんでした')
        print('保存できませんでした')
        return super().form_invalid(form)

# 実績入力画面 (UC-02)
class RequestLoginView(TemplateView):
    model = Request
    template_name = 'management_system/request_login.html'

    def post(self, request, *args, **kwargs):
        request_id = self.request.POST.get('request_id')
        request = get_object_or_404(Request, pk=request_id)
        print(self.request.POST.get("password"))
        print(type(self.request.POST.get("password")))
        print(request.password)
        print(type(request.password))
        if(int(self.request.POST.get("password")) == request.password ):
            print('login sucsess')
            print('loginId:' + request_id)
            return HttpResponseRedirect(reverse('performance', kwargs = {'pk':request_id}))
        else:
            print('login fail')
            return HttpResponseRedirect(reverse('login'))
        
    def get_context_data(self, **kwarg):
        print('make forms')
        context = super().get_context_data(**kwarg)
        context['form_id'] = RequestIdForm()
        context['form_password'] = RequestPasswordForm()
        return context

# 実績入力画面 (UC-02)
class RequestPerformanceView(TemplateView):
    model = Request
    template_name = 'management_system/request_performance.html'
    success_url = 'main/'

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if 'hello' in request.POST:
            print('hello')

        print("entry")
        print("self")
        print(self)
        print("request")
        print(request)
        print("args")
        print(args)
        print("kwargs")
        print(kwargs)
        request = get_object_or_404(Request,pk=kwargs.get('pk'))
        request.entry_datetime = timezone.localtime()
        request.save()
        print (request)
        
        return HttpResponseRedirect(reverse('main'))

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        print('getRequest')

        if( kwarg.get('pk') == None ):
            print('get false')
            return HttpResponseRedirect(reverse('login'))
            
        else:  
            print('getSucsess')
            request = get_object_or_404(Request,pk=kwarg.get('pk'))
            customer = get_object_or_404(Customer,pk=request.request_id)
            
            context['form_id'] = {'request_id':kwarg.get('pk')}

            context['form_request'] = request

            context['form_customer'] = customer

        return context

