from django.urls import path
from .views import RequestAddView , RequestMainView ,RequestPerformanceView , RequestLoginView, RequestFixView ,RequestFixLoginView , AdminApprovalView,RequestAddFinishView ,RequestPerformanceFinishView
from .views import AdminLoginView, RequestListView

from . import views

urlpatterns = [
    path('', RequestMainView.as_view(), name='main'),
    path('add/', RequestAddView.as_view(),name='add'), 
    path('add/finish/', RequestAddFinishView.as_view(),name='addfinish'), 
    path('login/',RequestLoginView.as_view(),name='login'),
    path('performance/<int:pk>/', RequestPerformanceView.as_view(),name='performance'), 
    path('performance/finish/', RequestPerformanceFinishView.as_view(),name='performancefinish'), 
    path('admin/login/',AdminLoginView.as_view(),name='admin_login'),
    path('admin/list/',RequestListView.as_view(),name='admin_list'),
    path('admin/approval/<int:pk>',AdminApprovalView.as_view(),name='admin_approval'),
    path('fix/login/',RequestFixLoginView.as_view(),name='fixlogin'),
    path('fix/<int:pk>', RequestFixView.as_view(),name='fix'),
]

