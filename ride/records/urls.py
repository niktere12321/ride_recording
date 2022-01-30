from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'records'


urlpatterns = [
    path(r'', views.CalendarView.as_view(), name='index'),
    path(r'records/', views.records, name='records'),
    url(r'^records/edit/(?P<records_id>\d+)/$', views.records, name='records_edit'),
]
