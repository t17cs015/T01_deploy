from django.http import HttpResponse

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
    fields = ('scheduled_entry_datetime', 'scheduled_exit_datetime', 'purpose_admission', 'email')
    template_name = 'management_system/request_add.html'
    success_url = '/'


