from django.contrib import messages  # メッセージフレームワーク
from django.http import HttpResponseRedirect
from django.shortcuts import redirect , get_object_or_404 , render
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime,pytz,random, string

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView , UpdateView
from django.views.generic import ListView
from .forms import RequestForm , RequestIdForm , RequestPasswordForm , RequestGetForm
from .forms import CustomerForm, AdminLoginForm

from .models import Request , Customer

class RequestMainView(TemplateView):
    template_name = 'management_system/request_main.html'

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
        print(self.request.POST.get('password'))
        print(type(self.request.POST.get('password')))
        print(request.password)
        print(type(request.password))
        if(int(self.request.POST.get('password')) == request.password ):
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
            
        print('entry')
        print('self')
        print(self)
        print('request')
        print(request)
        print('args')
        print(args)
        print('kwargs')
        print(kwargs)

        request = get_object_or_404(Request,pk=kwargs.get('pk'))
        if(request.entry_datetime==None):
            request.entry_datetime = timezone.localtime()
        elif(request.exit_datetime==None):
            request.exit_datetime = timezone.localtime()
        else:
            print('already logined')
            return HttpResponseRedirect(reverse('main'))
        request.save()
        print (request)
        
        #         request_id = self.request.POST.get('request_id')
        # request = get_object_or_404(Request, pk=request_id)
        # request.entry_datetime = timezone.localtime()

        # request_id = self.request.POST.get('request_id')
        # scheduled_entry_datetime = self.request.POST.get('scheduled_entry_datetime')
        # scheduled_exit_datetime = self.request.POST.get('scheduled_exit_datetime')
        # entry_datetime = self.request.POST.get('entry_datetime')

        # request = get_object_or_404(Request, pk=request_id)
        # request.scheduled_entry_datetime = scheduled_entry_datetime
        # request.scheduled_exit_datetime = scheduled_exit_datetime
        # request.entry_datetime = entry_datetime
        # request.save()
        return HttpResponseRedirect(reverse('login'))

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        print('getRequest')

        if( kwarg.get('pk') == None ):
            print('get false')
            # context['form_id'] = RequestIdForm()
            # context['form'] = RequestForm()
            
        else:  
            print('getSucsess')
            request = get_object_or_404(Request,pk=kwarg.get('pk'))
            customer = get_object_or_404(Customer,pk=request.request_id)
            context['form_id'] = {'request_id':kwarg.get('pk')}
            context['form_request'] = request
            context['form_customer'] = customer
            if(request.entry_datetime == None):
                context['form_message'] = "入館"
            elif(request.exit_datetime==None):
                context['form_message'] = "退館"
            else:
                print('already logined')

        return context

    def entry(self, **kwargs):
        print('hello')
        request_id = self.request.POST.get('request_id')
        request = get_object_or_404(Request, pk=request_id)
        request.entry_datetime = timezone.localtime()
        request.save()

        return request_id
        # return HttpResponseRedirect(reverse('performance', kwargs = {'pk':request_id}))

    def exit(self, **kwargs):
        return

class AdminLoginView(LoginView):
    form_class = AdminLoginForm
    next = 'admin_list'
    template_name = 'management_system/admin_login.html'

class RequestListView(LoginRequiredMixin, ListView):
    model = Request
    login_url = 'admin_login'
    template_name = 'management_system/admin_list.html'

    def get_context_data(self, **kwargs):
        context = super(RequestListView, self).get_context_data(**kwargs)
        return context


