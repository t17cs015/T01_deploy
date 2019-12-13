from django.urls import path
from .views import RequestAddView

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:request_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:request_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:request_id>/vote/', views.vote, name='vote'),

    path('add/', RequestAddView.as_view(),name='add'), 
]