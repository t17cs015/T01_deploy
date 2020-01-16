from django.contrib import messages
from django.core.mail import BadHeaderError , send_mail
from django.http import HttpResponseRedirect , QueryDict
from django.shortcuts import redirect , get_object_or_404 , render
from django.utils import timezone
from django.urls import reverse,path

import datetime,pytz,random, string

from django.views.generic.base import TemplateView
from . import views
from django.views.generic.edit import CreateView , UpdateView , FormView
from .forms import RequestForm , RequestIdForm , RequestPasswordForm , RequestSendForm
from .forms import CustomerForm


from .models import Request , Customer

class RequestMainView(TemplateView):
    template_name = 'management_system/request_main.html'

# 入館申請画面 (UC-01)
class RequestAddView(FormView):
    model = Request
    template_name = 'management_system/request_add.html'
    success_url = '/management_system'
    form_class = RequestSendForm
    # second_form_class = CustomerForm


    def form_valid(self,form):
        print('baride-syonn')
        # print(form)
        # print(form.name)
        # print(form.get('name'))
        print(form.cleaned_data['name'])
        context = {
            'form' : form
        }

        return render(self.request,'management_system/request_add_check.html' ,context)
        # return super().form_valid(form)

    
    def post(self, request, *args, **kwargs):
        print('post')



        return super().post(request, *args, **kwargs)

    # def get_context_data(self,**kwargs):
    #     context = super(FormView, self).get_context_data(**kwargs)
    #     print(context)
    #     context['form_Request'] = RequestForm()
    #     context['form_Customer'] = CustomerForm()
    #     print(context)
    #     return context

    # def post(self, request, *args, **kwargs):
    #     print('addCheck viewwww')
    #     print('self')
    #     print(self)
    #     print('request')
    #     print(request)
    #     print('args')
    #     print(args)
    #     print('kwargs')
    #     print(kwargs)

    #     print('POST')
    #     print(request.POST)
    #     print('GET')
    #     print(request.GET)

    #     print(request.POST.get('scheduled_entry_datetime'))
        
    #     entrys = request.POST.get('scheduled_entry_datetime')
    #     exits = request.POST.get('scheduled_exit_datetime')

    #     print(type(request.POST.get('tell_number')))

    #     entryt= timezone.datetime.strptime(entrys,'%Y-%m-%dT%H:%M')
    #     exitt = timezone.datetime.strptime(exits,'%Y-%m-%dT%H:%M')

    #     print(entryt)

    #     jp = pytz.timezone('Asia/Tokyo')
    #     print(jp.localize(exitt))

    #     en = str(jp.localize(entryt))
    #     ex = str(jp.localize(exitt))


    #     queryd = QueryDict('scheduled_entry_datetime='+en[0:19]+'&scheduled_exit_datetime='+ex[0:19]+'&purpose_admission='+request.POST.get('purpose_admission'),mutable=True)
    #     # queryd = QueryDict('purpose_admission=a',mutable=True)
    #     print('querydict')
    #     print(queryd)

    #     customer = self.second_form_class(request.POST)
    #     req = self.form_class(queryd)
        
    #     print(req)

    #     kwargs = {
    #         'form_Request' : req,
    #         'form_Customer': customer,
    #     }
    #     context = kwargs
    #     # context['form_Request'] = RequestForm()
    #     # context = {
    #     #     'organization_name': request.POST.get('organization_name'),
    #     #     'name': request.POST.get('name'),
    #     #     'tell_number': request.POST.get('tell_number'),
    #     #     'email': request.POST.get('email'),
    #     #     'scheduled_entry_datetime': request.POST.get('scheduled_entry_datetime'),
    #     #     'scheduled_exit_datetime': request.POST.get('scheduled_exit_datetime'),
    #     #     'purpose_admission': request.POST.get('purpose_admission'),
    #     # }
        
        
    #     print('contex:')
    #     print(context)
    #     print(context['form_Request'])
    #     print(context['form_Customer'])
        
    #     return render(request,'management_system/request_add_check.html' ,context)
    #     # return HttpResponseRedirect(render(context, request))
    
# 入館申請画面 (UC-01)
class RequestAddCheckView(CreateView):
    model = Request
    template_name = 'management_system/request_add.html'
    success_url = ''
    # form_class = RequestForm
    # second_form_class = CustomerForm

    def form_valid(self,form):
        print('baride-syonn')


        return super().form_valid(form)

    
    def post(self, request, *args, **kwargs):
        print('post')


        return super().post(request, *args, **kwargs)
    


    # def post(self, request, *args, **kwargs):        
    #     form = self.form_class(request.POST)
        # form2 = self.second_form_class(request.POST)

        # print('form1')
        # print(form1)
        # print('form2')
        # print(form2)

        # print(request.POST.get('scheduled_entry_datetime')) 
        # print(type(request.POST.get('scheduled_entry_datetime')))

        # entrys = request.POST.get('scheduled_entry_datetime')
        # exits = request.POST.get('scheduled_exit_datetime')

        # if form1.is_valid():
        # obj1 = form1.save(commit=False)
        # obj2 = form2.save(commit=False)
        # obj1 = obj2

        # entryt= timezone.datetime.strptime(entrys,'%Y-%m-%dT%H:%M')
        # exitt = timezone.datetime.strptime(exits,'%Y-%m-%dT%H:%M')

        # jp = pytz.timezone('Asia/Tokyo')
        # print(jp.localize(exitt))

        # obj1.scheduled_entry_datetime = jp.localize(entryt)
        # obj1.scheduled_exit_datetime = jp.localize(exitt)
        
    #     # 入館時間よりも退館時間の方が前の時、申請を受け付けない
    #     if obj1.scheduled_entry_datetime >= obj1.scheduled_exit_datetime:
    #         messages.success(self.request, '入力時間が正しくありません')
    #         return HttpResponseRedirect(reverse('add'))

    #     # emailに該当するものをすべて取得
    #     customers = list(Customer.objects.filter(email=obj2.email))
        
    #     if(len(customers)==0):
    #         print('一致するメアドがlistに存在しない')
    #     else:
    #         print('一致するメアドがlistに存在する')
    #     print('request')
    #     print(request)
    #     print('customers')
    #     print(customers)

    #     # listの判別
    #     hit = 0

    #     for cus in customers:
    #         print(cus.tell_number)
    #         if(cus.name == obj2.name and cus.organization_name == obj2.organization_name and cus.tell_number == obj2.tell_number):
    #             # そのままcustomerを使う
    #             print('全件一致しました')
    #             obj2 = cus
    #             hit = 1
    #         else:
    #             # Customerを入力のものと置き換える
    #             print('このデータは全件一致しませんでした')
        
    #     # 一致しなかったときにustomerをRequestに保持させる
    #     if(hit == 0):
    #         customer = Customer
    #         # カスタマーの追加とそれを引数に渡す
    #         obj2.save()
    #         print('customer save')
        
    #     obj1.email = obj2
    #     obj1.request_datetime = timezone.localtime()

    #     # 入館時間が現在時刻よりも前の場合は申請を受け付けない
    #     if obj1.scheduled_entry_datetime < obj1.request_datetime:
    #         messages.success(self.request, '過去の時間に入館申請はできません')
    #         return HttpResponseRedirect(reverse('add'))

    #     obj1.password = ''.join([random.choice(string.digits) for i in range(4)])
    #     print(obj1.scheduled_entry_datetime)
    #     print(obj2)

    #     # 時間の判定
    #     # 承認済みの時間にかぶせて申請が入った場合のみ削除
    #     # 過去の日時の申請もきっとはじいた方がいいかも？

    #     # 申請されたものの入館時間より早い入館時間を持ち、遅い退館時間を持つもの
    #     # 及び退館時間も同様
    #     # 以上の二点に該当するものをfilterで持ってくる
    #     requests = list(filter(lambda x:True if(obj1.scheduled_entry_datetime >= x.scheduled_entry_datetime and obj1.scheduled_entry_datetime < x.scheduled_exit_datetime) else False ,Request.objects.all()))
    #     print(requests)
    #     requests += list(filter(lambda x:True if(obj1.scheduled_exit_datetime > x.scheduled_entry_datetime and obj1.scheduled_exit_datetime <= x.scheduled_exit_datetime) else False ,Request.objects.all()))
    #     print(requests)
    #     if(len(requests) != 0):
    #         for req in requests:
    #             if(req.approval == 1):
    #                 print('すでに申請されている時間帯なのでこの時間は申請できません')
    #                 print(req)
    #                 messages.success(self.request, 'すでに申請されている時間帯なのでこの時間は申請できません')
    #                 return HttpResponseRedirect(reverse('add'))
    #     obj1.save()

    #     print('save')
    #     obj1.request_id = obj1.id
    #     print('dainyuu')
    #     obj1.save()
        
    #     print('obj1.id')
    #     print(obj1.id)
    #     print('obj2.id')
    #     print(obj2.id)
    #     print('Ill send')
    #     return self.form_valid(form1,obj1)
    # # else:
    # #     return self.form_invalid(form1,obj1)

    def form_valid(self, form,obj):
        print('保存しました')

        subject = ' W社DC利用申請受領のお知らせ'
        massage = obj.email.organization_name+' '+ obj.email.name + '様\n\n'+'お世話になっております。\nW社でございます。\n\n以下の内容でのデータセンターの利用申請を受け付け致しました。\n申請の承認につきましては、管理者が確認後再度連絡させていただきます。\n\n------利用申請内容------\n申請日時 : ' + obj.request_datetime.strftime('%Y/%m/%d %H:%M:%S') + '\n入館予定日時 : '+obj.scheduled_entry_datetime.strftime('%Y/%m/%d %H:%M:%S') +'\n退館予定日時 : ' + obj.scheduled_exit_datetime.strftime('%Y/%m/%d %H:%M:%S') + '\n------------------------------\n\nそれに伴い' + obj.email.name + '様の申請番号を以下に記載いたします。\n\n申請番号 : ' + str(obj.request_id) + '\n\n申請番号は入退館時に必要になりますので厳重に保管下さい。\n\nまた、利用申請が承認されていない状態であれば下記URLで申請内容の修正、取消が行えます。\n\nURL : http://example.com/3020\n\n------------------------------\n署名\n------------------------------\n\n本メールは”データセンター入退館管理システム”からの自動送信です。\n'
        from_email = 'dbcenterw1@gmail.com'
        recipient_list = [
            obj.email.__str__()
        ]
        print('send mail')
        send_mail(subject,massage,from_email,recipient_list)
        messages.success(self.request, '申請を受理しました')

        return super().form_valid(form)

        

    # def entry(self, **kwargs):
    #     print('hello')
    #     request_id = self.request.POST.get('request_id')
    #     request = get_object_or_404(Request, pk=request_id)
    #     request.entry_datetime = timezone.localtime()
    #     request.save()

    #     return request_id
    #     # return HttpResponseRedirect(reverse('performance', kwargs = {'pk':request_id}))
   

   

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
            return HttpResponseRedirect(reverse('main'))
        request.save()
        print (request)
        

        return HttpResponseRedirect(reverse('login'))

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
            customer = get_object_or_404(Customer,pk=request.request_id)
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

