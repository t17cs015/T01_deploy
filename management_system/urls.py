from django.urls import path
from .views import RequestAddView , RequestMainView ,RequestPerformanceView , RequestLoginView, RequestFixView

from . import views

urlpatterns = [
    path('main/', RequestMainView.as_view(), name='main'),
    # ex: /polls/5/
    # path('<int:request_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    # path('<int:request_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    # path('<int:request_id>/vote/', views.vote, name='vote'),
    path('add/', RequestAddView.as_view(),name='add'), 
    path('login/',RequestLoginView.as_view(),name='login'),
    path('performance/<int:pk>/', RequestPerformanceView.as_view(),name='performance'), 
    path('fix/', RequestFixView.as_view(),name='fix'),
]