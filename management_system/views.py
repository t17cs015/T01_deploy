from django.contrib import messages
from django.core.mail import BadHeaderError , send_mail
from django.http import HttpResponseRedirect , QueryDict
from django.shortcuts import redirect , get_object_or_404 , render
from django.utils import timezone
from django.urls import reverse,path
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime,pytz,random, string

from django.views.generic.base import TemplateView
from . import views
from django.views.generic.edit import CreateView , UpdateView , FormView
from django.views.generic import ListView
from django import forms
from .forms import RequestForm , RequestIdForm , RequestPasswordForm , RequestGetForm , RequestSendForm
from .forms import CustomerForm, AdminLoginForm

from .models import Request , Customer
import copy

class RequestMainView(TemplateView):
    template_name = 'management_system/request_main.html'

# 入館申請画面 (UC-01)
class RequestAddView(FormView):
    model = Request
    template_name = 'management_system/request_add.html'
    success_url = '/management_system/add/finish/'
    form_class = RequestSendForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        # form.fields['name'].widget = forms.CheckboxSelectMultiple()
        print(form.errors)
        return form

    def form_valid(self,form):
        context = {
            'form' : form
        }
        if self.request.POST.get('next', '') == 'confirm':
            req = RequestForm(self.request.POST).save(commit=False)
            # 申請されたものの入館時間より早い入館時間を持ち、遅い退館時間を持つもの
            # 及び退館時間も同様
            # 以上の二点に該当するものをfilterで持ってくる
            requests = list(filter(lambda x:True if(req.scheduled_entry_datetime >= x.scheduled_entry_datetime and req.scheduled_entry_datetime < x.scheduled_exit_datetime) else False ,Request.objects.all()))
            requests += list(filter(lambda x:True if(req.scheduled_exit_datetime > x.scheduled_entry_datetime and req.scheduled_exit_datetime <= x.scheduled_exit_datetime) else False ,Request.objects.all()))
            print(requests)
            hit = 0
            cus_hit = 0
            if(len(requests) != 0):
                for req in requests:
                    if(req.approval == 1):
                        print('承認済みの申請と時間が被りました')
                        # listの判別
                        cus = req.email
                        if(cus.email == self.request.POST.get('email') and cus.name == self.request.POST.get('name') and cus.organization_name == self.request.POST.get('organization_name') and cus.tell_number == self.request.POST.get('tell_number')):
                            # そのままcustomerを使う
                            print(str(cus.id)+' 全件一致しました')
                            print('あなたの申請がこの時間に入っています')
                            customer = cus
                            cus_hit = 1
                        else:
                            # Customerを入力のものと置き換える
                            print(str(cus.id)+' このデータは全件一致しませんでした')
                            hit = 1
            if(hit == 1):
                messages.success(self.request, 'すでに申請されている時間帯なのでこの時間は申請できません')
                context['form_message'] = '重複'
                print('すでに申請されている時間帯なのでこの時間は申請できません')
                print(req)
            elif(cus_hit == 1):
                messages.success(self.request, 'あなたの申請がこの時間に入っています')
            return render(self.request, 'management_system/request_add_check.html', context)

        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'management_system/request_add.html', context)
        if self.request.POST.get('next', '') == 'create':
            # 入力されたものに対してオブジェクトを生成
            req = RequestForm(self.request.POST).save(commit=False)
            cust = CustomerForm(self.request.POST).save(commit=False)
            # 入館時間が現在時刻よりも前の場合は申請を受け付けない
            if req.scheduled_entry_datetime < timezone.localtime():
                messages.success(self.request, '過去の時間に入館申請はできません')
                return render(self.request, 'management_system/request_add.html', context)
            # 入館時間よりも退館時間の方が前の時、申請を受け付けない
            if req.scheduled_entry_datetime >= req.scheduled_exit_datetime:
                messages.success(self.request, '入力時間が正しくありません')
                return render(self.request, 'management_system/request_add.html', context)
            # 時間の判定
            # 承認済みの時間にかぶせて申請が入った場合のみはじく

            # emailに該当するものをすべて取得
            customers = list(Customer.objects.filter(email=self.request.POST.get('email')))
            # listの判別
            hit = 0
            for cus in customers:
                # print(cus.tell_number)
                if(cus.name == cust.name and cus.organization_name == self.request.POST.get('organization_name') and cus.tell_number == self.request.POST.get('tell_number')):
                    # そのままcustomerを使う
                    print(str(cus.id)+' 全件一致しました')
                    customer = cus
                    hit = 1
                else:
                    # Customerを入力のものと置き換える
                    print(str(cus.id)+' このデータは全件一致しませんでした')
            
            # 一致しなかったときにustomerをRequestに保持させる
            if(hit == 0):
                customer = cust
                # カスタマーの追加とそれを引数に渡す

            customer.save()
            req.password = ''.join([random.choice(string.digits) for i in range(4)])
            req.email = customer
            req.request_datetime = timezone.localtime()
            req.save()

            self.sendMail(form,req)
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('base:main'))

    def sendMail(self, form,req):
        print('保存しました')

        subject = ' W社DC利用申請受領のお知らせ'
        massage = req.email.organization_name+' '+ req.email.name + '様\n\n'+'お世話になっております。\nW社でございます。\n\n以下の内容でのデータセンターの利用申請を受け付け致しました。\n申請の承認につきましては、管理者が確認後再度連絡させていただきます。\n\n------利用申請内容------\n申請日時 : ' + req.request_datetime.strftime('%Y/%m/%d %H:%M:%S') + '\n入館予定日時 : '+req.scheduled_entry_datetime.strftime('%Y/%m/%d %H:%M:%S') +'\n退館予定日時 : ' + req.scheduled_exit_datetime.strftime('%Y/%m/%d %H:%M:%S') + '\n------------------------------\n\nそれに伴い' + req.email.name + '様の申請番号とパスワードを以下に記載いたします。\n\n申請番号 : ' + str(req.pk) + '\nパスワード : '+ str(req.password)  +'\n\n申請番号は入退館時に必要になりますので厳重に保管下さい。\n\nまた、利用申請が承認されていない状態であれば下記URLで申請内容の修正、取消が行えます。\n\nURL : http://t17cs015.pythonanywhere.com/management_system/fix/login/\n\n------------------------------\nW社 DCセンター管理部\ndbcenterw01@gmail.com\n------------------------------\n\n本メールは”データセンター入退館管理システム”からの自動送信です。\n'
        from_email = 'dbcenterw1@gmail.com'
        recipient_list = [
            req.email.__str__()
        ]
        print('send mail')
        send_mail(subject,massage,from_email,recipient_list)
        # messages.success(self.request, '申請を受理しました')

        return 0

    # 元addcheck
    # カレンダー関係のだけ残ってます

    # def post(self, request, *args, **kwargs):        
  
        # print(request.POST.get('scheduled_entry_datetime')) 
        # print(type(request.POST.get('scheduled_entry_datetime')))

        # entrys = request.POST.get('scheduled_entry_datetime')
        # exits = request.POST.get('scheduled_exit_datetime')

        # entryt= timezone.datetime.strptime(entrys,'%Y-%m-%dT%H:%M')
        # exitt = timezone.datetime.strptime(exits,'%Y-%m-%dT%H:%M')

        # jp = pytz.timezone('Asia/Tokyo')
        # print(jp.localize(exitt))

        # req1.scheduled_entry_datetime = jp.localize(entryt)
        # obj1.scheduled_exit_datetime = jp.localize(exitt)

# 申請送信完了後の画面(UC-01)
class RequestAddFinishView(TemplateView):
    template_name = 'management_system/request_add_finish.html'
    success_url = '/management_system/add'
           
# 実績入力完了後の画面(UC-02)
class RequestPerformanceFinishView(TemplateView):
    template_name = 'management_system/request_performance_check.html'
    success_url = '/management_system/login'

    def get_context_data(self, **kwarg):
            context = super().get_context_data(**kwarg)
            context['time'] = timezone.localtime()
            print('time')
            print(context['time'])
            return context

    def post(self, request, *args, **kwargs):
        return render(self.request, 'management_system/request_login.html', context)

# 実績入力画面 (UC-02)
class RequestLoginView(TemplateView):
    model = Request
    template_name = 'management_system/request_login.html'

    def post(self, request, *args, **kwargs):
        request_id = self.request.POST.get('request_id')
        requests = list(Request.objects.filter(id=request_id))
        if len(requests) == 0:
            print('このidは存在しません')
            messages.success(self.request, 'idとパスワードが一致しません')
            return HttpResponseRedirect(reverse('login'))

        request = get_object_or_404(Request, pk=request_id)
        print('入力されたpas : ' + self.request.POST.get('password'))
        print('本来のpas : ' + str(request.password))
        print('入館時間 : ' + str(request.entry_datetime))
        print('退館時間 : ' + str(request.exit_datetime))
        
        if(int(self.request.POST.get('password')) != request.password ):
            print('login fail')
            messages.success(self.request, 'idとパスワードが一致しません')
            return HttpResponseRedirect(reverse('login'))

        elif(request.entry_datetime!=None and request.exit_datetime!=None):
            print('この申請は既に退館済みです')
            messages.success(self.request, 'この申請は既に退館済みです')
            return HttpResponseRedirect(reverse('login'))
        elif(request.approval == 0):
            print('この申請は承認前のため入館できません')
            messages.success(self.request, 'この申請は承認前のため入館できません')
            return HttpResponseRedirect(reverse('login'))
        else:
            print('login sucsess')
            print('loginId:' + request_id)
            return HttpResponseRedirect(reverse('performance', kwargs = {'pk':request_id}))
        
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
            return HttpResponseRedirect(reverse('login'))
        request.save()
        print (request)
        

        return HttpResponseRedirect(reverse('performancefinish'))

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        print('getRequest')

        if( kwarg.get('pk') == None ):
            print('get false')
            messages.success(self.request, 'idに一致するものが存在しませんでした')
            return context
        else:  
            print('getSucsess')
            request = get_object_or_404(Request,pk=kwarg.get('pk'))
            customer = get_object_or_404(Customer,pk=request.email.pk)
            print(request)

            
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
    
# 実績修正画面ログイン (UC-05)
class RequestFixLoginView(TemplateView):
    model = Request
    template_name = 'management_system/request_login.html'

    def post(self, request, *args, **kwargs):
        request_id = self.request.POST.get('request_id')
        requests = list(Request.objects.filter(id=request_id))
        if len(requests) == 0:
            print('このidは存在しません')
            messages.success(self.request, 'idとパスワードが一致しません')
            return HttpResponseRedirect(reverse('fixlogin'))

        request = get_object_or_404(Request, pk=request_id)
        print('入力されたpas : ' + self.request.POST.get('password'))
        print('本来のpas : ' + str(request.password))
        print('入館時間 : ' + str(request.entry_datetime))
        print('退館時間 : ' + str(request.exit_datetime))
        
        if(int(self.request.POST.get('password')) != request.password ):
            print('login fail')
            messages.success(self.request, 'idとパスワードが一致しません')
            return HttpResponseRedirect(reverse('fixlogin'))
        
        # ここは未承認かの判定にしたい
        if(request.approval!=0):
            print('この申請は既に承認済みです')
            messages.success(self.request, 'この申請は既に承認済みのため修正できません')
            return HttpResponseRedirect(reverse('fixlogin'))
        
        else:
            print('login sucsess')
            print('loginId:' + request_id)
            return HttpResponseRedirect(reverse('fix', kwargs = {'pk':request_id}))
        
    def get_context_data(self, **kwarg):
        print('make forms')
        context = super().get_context_data(**kwarg)
        context['form_id'] = RequestIdForm()
        context['form_password'] = RequestPasswordForm()
        return context

# 実績修正画面 (UC-05)
class RequestFixView(UpdateView):
    model = Request
    template_name = 'management_system/request_fix.html'
    success_url = '../fix/login'
    # form = RequestSendForm
    fields = ['scheduled_entry_datetime', 'scheduled_exit_datetime', 'purpose_admission']
    cust = Customer

    def get_context_data(self, **kwarg):
        print('make forms:RexestFix')
        context = super().get_context_data(**kwarg)
        self.cust = Customer(context['object'].email)
        
        return context

    def form_valid(self,form):
        context = {
            'form' : form
        }

        self.object = self.get_object()
        print(self.object.email.email)
        print(self.request.POST.get('email'))
        if(self.object.email.email == self.request.POST.get('email')):
            if(self.object.email.name == self.request.POST.get('name')):
                if(self.object.email.organization_name == self.request.POST.get('organization_name')):
                    if(self.object.email.tell_number == self.request.POST.get('tell_number')):
                        print('以前申請したものと全件一致しました')
                        self.sendMail(self.object)
                        return super().form_valid(form)
        
        print('顧客情報が修正されたのでDBを確認します')

        # emailに該当するものをすべて取得
        customers = list(Customer.objects.filter(email=self.request.POST.get('email')))
        # listの判別
        hit = 0
        for cus in customers:
            # print(cus.tell_number)
            if(cus.name == self.request.POST.get('name') and cus.organization_name == self.request.POST.get('organization_name') and cus.tell_number == self.request.POST.get('tell_number')):
                # そのままcustomerを使う
                print(str(cus.id)+' 全件一致しました')
                customer = cus
                hit = 1
            else:
                # Customerを入力のものと置き換える
                print(str(cus.id)+' このデータは全件一致しませんでした')
        
        # 一致しなかったときにcustomerをRequestに保持させる
        if(hit == 0):
            # customer = self.cust
            customer = CustomerForm(self.request.POST).save()
        
        # カスタマーの追加とそれを引数に渡す
        print(hit)
        self.object = form.save(commit=False)
        self.object.email = customer
        print(self.object.email.id)
        print(self.object)
        self.object.save()

        self.sendMail(self.object)
        
        return HttpResponseRedirect(self.get_success_url())
    
    def sendMail(self, req):
        print('保存しました')

        subject = ' W社DC利用修正受領のお知らせ'
        massage = req.email.organization_name+' '+ req.email.name + '様\n\n'+'お世話になっております。\nW社でございます。\n\n以下の内容でのデータセンターの利用修正を受け付け致しました。\n申請修正の承認につきましては、管理者が確認後再度連絡させていただきます。\n\n------利用申請内容------\n申請日時 : ' + req.request_datetime.strftime('%Y/%m/%d %H:%M:%S') + '\n入館予定日時 : '+req.scheduled_entry_datetime.strftime('%Y/%m/%d %H:%M:%S') +'\n退館予定日時 : ' + req.scheduled_exit_datetime.strftime('%Y/%m/%d %H:%M:%S') + '\n------------------------------\n\nそれに伴い' + req.email.name + '様の申請番号、パスワードは以前発行したとおりです\n'  + '\n\n申請番号、パスワードは入退館時に必要になりますので厳重に保管下さい。\n\nまた、利用申請が承認されていない状態であれば下記URLで申請内容の修正、取消が行えます。\n\nURL : http://t17cs015.pythonanywhere.com/management_system/fix/login/\n\n------------------------------\nW社 DCセンター管理部\ndbcenterw01@gmail.com\n------------------------------\n\n本メールは”データセンター入退館管理システム”からの自動送信です。\n'
        from_email = 'dbcenterw1@gmail.com'
        recipient_list = [
            req.email.__str__()
        ]
        print('send mail')
        send_mail(subject,massage,from_email,recipient_list)
        messages.success(self.request, '修正を受理しました')

        return 0

class AdminLoginView(LoginView):
    form_class = AdminLoginForm
    next = 'admin_list'
    template_name = 'management_system/admin_login.html'

class RequestListView(LoginRequiredMixin, ListView):
    model = Request
    login_url = 'admin_login'
    template_name = 'management_system/admin_list.html'
    ascending_order = False
    searched_string = ""

    def get_context_data(self, **kwargs):
        context = super(RequestListView, self).get_context_data(**kwargs)

        context["ascending_order"] = "true" if self.ascending_order == True else "false"
        context["searched_string"] = self.searched_string

        return context

    def get_queryset(self):
        results = self.model.objects.all()

        q_name = self.request.GET.get('name')
        q_order = self.request.GET.get('order')

        if q_name is not None:
            results = results.filter(email__organization_name__contains=q_name)
            self.searched_string = q_name
        else:
            self.searched_string = ""

        if q_order == "desce":
            self.ascending_order = False
            results = results.order_by("request_datetime").reverse()
        elif q_order == "asce":
            self.ascending_order = True
            results = results.order_by("request_datetime")

        return results

# 申請承認画面 
class AdminApprovalView(TemplateView):
    model = Request
    template_name = 'management_system/admin_approval.html'
    success_url = ''

    def form_valid(self,form):
        print('form')
        print(form)
        return super().form_valid(form)

    def form_invalid(self,form):
        print('form')
        print(form)
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        print('self')
        print(self)
        print('request')
        print(request)
        print(request.POST)
        print('args')
        print(args)
        print('kwargs')
        print(kwargs)
        
        # 承認データの取得
        req = get_object_or_404(Request,pk=kwargs.get('pk'))

        # 承認がクリックされた場合の処理
        if 'approval' in request.POST:
            requests = list(filter(lambda x:True if(req.scheduled_entry_datetime >= x.scheduled_entry_datetime and req.scheduled_entry_datetime < x.scheduled_exit_datetime) else False ,Request.objects.all()))
            requests += list(filter(lambda x:True if(req.scheduled_exit_datetime > x.scheduled_entry_datetime and req.scheduled_exit_datetime <= x.scheduled_exit_datetime) else False ,Request.objects.all()))
            print(requests)
            if(len(requests) != 0):
                for requ in requests:
                    if(requ.approval == 1):
                        print('すでに申請されている時間帯なのでこの時間は申請できません')
                        print(requ)
                        messages.success(self.request, 'すでに申請されている時間帯なのでこの時間は申請できません')
                        return HttpResponseRedirect(reverse('admin_approval' , kwargs={'pk':kwargs.get('pk')}))

            print('承認します')
            req.approval = 1
            messages.success(self.request, 'id:'+str(kwargs.get('pk'))+'の申請を承認しました')
        # 拒否がクリックされた場合の処理
        if 'noapproval' in request.POST:
            req.approval = 0
            messages.success(self.request, 'id:'+str(kwargs.get('pk'))+'の申請を拒否しました')
            print('拒否します')


        req.save()
        print (req)
        return HttpResponseRedirect(reverse('admin_list'))
    
    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        print('getRequest')

        if( kwarg.get('pk') == None ):
            print('get false')
            messages.success(self.request, 'idに一致するものが存在しませんでした')
            return context
        else:  
            print('getSucsess')
            request = get_object_or_404(Request,pk=kwarg.get('pk'))
            customer = get_object_or_404(Customer,pk=request.email.pk)
            print(request)

            context['form_id'] = {'request_id':kwarg.get('pk')}
            context['form_request'] = request
            context['form_customer'] = customer
            context['form_message'] = '承認'
            
        return context
