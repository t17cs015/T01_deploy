from django.urls import path
from .views import RequestAddView , RequestMainView ,RequestPerformanceView , RequestLoginView, RequestFixView ,RequestFixLoginView , AdminApprovalView
from .views import AdminLoginView, RequestListView

from . import views

urlpatterns = [
    path('', RequestMainView.as_view(), name='main'),
    # ex: /polls/5/
    # path('<int:request_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    # path('<int:request_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    # path('<int:request_id>/vote/', views.vote, name='vote'),
    path('add/', RequestAddView.as_view(),name='add'), 
    path('login/',RequestLoginView.as_view(),name='login'),
    path('performance/<int:pk>/', RequestPerformanceView.as_view(),name='performance'), 
    path('admin/login/',AdminLoginView.as_view(),name='admin_login'),
    path('admin/list/',RequestListView.as_view(),name='admin_list'),
    path('admin/approval/<int:pk>',AdminApprovalView.as_view(),name='admin_approval'),
    path('fix/login/',RequestFixLoginView.as_view(),name='fixlogin'),
    path('fix/<int:pk>', RequestFixView.as_view(),name='fix'),
]

