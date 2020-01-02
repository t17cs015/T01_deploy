from django.contrib import messages  # メッセージフレームワーク
from django.core.mail import BadHeaderError , send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect , get_object_or_404 , render
from django.utils import timezone
from django.urls import reverse,path

import datetime,pytz,random, string

from django.views.generic.base import TemplateView
from . import views
from django.views.generic.edit import CreateView , UpdateView
from .forms import RequestForm , RequestIdForm , RequestPasswordForm , RequestGetForm
from .forms import CustomerForm

from .models import Request , Customer

class RequestMainView(TemplateView):
    template_name = 'management_system/request_main.html'

# 入館申請画面 (UC-01)
class RequestAddView(CreateView):
    model = Request
    template_name = 'management_system/request_add.html'
    success_url = '/management_system'
    form_class = RequestForm
    second_form_class = CustomerForm

    def get_context_data(self,**kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['form_Request'] = RequestForm()
        context['form_Customer'] = CustomerForm()
        print(context)
        return context

    def post(self, request, *args, **kwargs):
        print('self')
        print(self)
        print('request')
        print(request)
        print('args')
        print(args)
        print('kwargs')
        print(kwargs)

        form1 = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)

        print('form1')
        print(form1)
        print('form2')
        print(form2)

        if form1.is_valid():
            obj1 = form1.save(commit=False)
            obj2 = form2.save(commit=False)
            # emailに該当するものをすべて取得
            customers = list(Customer.objects.filter(email=obj2.email))
            
            if(len(customers)==0):
                print('一致するメアドがlistに存在しない')
            else:
                print('一致するメアドがlistに存在する')
            print('request')
            print(request)
            print('customers')
            print(customers)

            # listの判別
            hit = 0

            for cus in customers:
                print(cus.tell_number)
                if(cus.name == obj2.name and cus.organization_name == obj2.organization_name and cus.tell_number == obj2.tell_number):
                    # そのままcustomerを使う
                    print('全件一致しました')
                    obj2 = cus
                    hit = 1
                else:
                    # Customerを入力のものと置き換える
                    print('このデータは全件一致しませんでした')
            
            # 一致しなかったときにustomerをRequestに保持させる
            if(hit == 0):
                customer = Customer
                # カスタマーの追加とそれを引数に渡す
                obj2.save()
                print('customer save')
            
            obj1.email = obj2
            obj1.request_datetime = timezone.localtime()
            obj1.password = ''.join([random.choice(string.digits) for i in range(4)])
            
            # 時間の判定
            # 承認済みの時間にかぶせて申請が入った場合のみ削除
            # 過去の日時の申請もきっとはじいた方がいいかも？

            # 申請されたものの入館時間より早い入館時間を持ち、遅い退館時間を持つもの
            # 及び退館時間も同様
            # 以上の二点に該当するものをfilterで持ってくる
            requests = list(filter(lambda x:True if(obj1.scheduled_entry_datetime >= x.scheduled_entry_datetime and obj1.scheduled_entry_datetime < x.scheduled_exit_datetime) else False ,Request.objects.all()))
            print(requests)
            requests += list(filter(lambda x:True if(obj1.scheduled_exit_datetime > x.scheduled_entry_datetime and obj1.scheduled_exit_datetime <= x.scheduled_exit_datetime) else False ,Request.objects.all()))
            print(requests)
            if(len(requests) != 0):
                for req in requests:
                    if(req.approval == 1):
                        print('すでに申請されている時間帯なのでこの時間は申請できません')
                        print(req)
                        return HttpResponseRedirect(reverse('add'))
            obj1.save()

            print('save')
            obj1.request_id = obj1.id
            print('dainyuu')
            obj1.save()
            
            print('obj1.id')
            print(obj1.id)
            print('obj2.id')
            print(obj2.id)
            print('Ill send')
            return self.form_valid(form1,obj1)
        else:
            return self.form_invalid(form1)

    def form_valid(self, form,obj):
        # messages.success(self.request, '保存しました')
        print('保存しました')

        subject = 'W DC Center'
        massage = obj.email.name+'さん\n\nW社です\n\nDBセンター利用ご予約を受け取りましたので報告いたします\n\n申請日時 : ' + obj.request_datetime.strftime('%Y/%m/%d %H:%M:%S') + '\n入館予定日時 : '+obj.scheduled_entry_datetime.strftime('%Y/%m/%d %H:%M:%S') +'\n退館予定日時 : '+obj.scheduled_exit_datetime.strftime('%Y/%m/%d %H:%M:%S') +'\n電話番号 : ' + obj.email.tell_number + '\n\n管理者が確認後、再度、メールを送信します\n本メールは自動送信により内容の確認を行うものであって、予約を保証するものではありません\n申請が取り消される場合がございます'
        from_email = 'dbcenterw1@gmail.com'
        recipient_list = [
            obj.email.__str__()
        ]
        print('send mail')
        send_mail(subject,massage,from_email,recipient_list)

        return super().form_valid(form)
    

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
    success_url = ''

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
            return HttpResponseRedirect(reverse(''))
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
            customer = get_object_or_404(Customer,pk=request.email.id)
            context['form_id'] = {'request_id':kwarg.get('pk')}
            context['form_request'] = request
            context['form_customer'] = customer
            if(request.entry_datetime == None):
                context['form_message'] = '入館'
            elif(request.exit_datetime==None):
                context['form_message'] = '退館'
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