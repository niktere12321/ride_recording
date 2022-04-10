from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'records'


urlpatterns = [
    path(r'', views.CalendarView.as_view(), name='index'),
    path(r'ship/', views.Calendar_shipView.as_view(), name='index_ship'),
    url(r'records/(?P<date>[0-9]{8})/$', views.records_start, name='records_start'),
    url(r'ship/records_ship/(?P<date>[0-9]{8})/$', views.records_ship_start, name='records_ship_start'),
    path('records/records/<int:rec_pk>/delete/', views.records_delete, name='records_delete'),
    path('records/profiles', views.profiles, name='profiles'),
    path('records/admining/<str:username>', views.admining_pk, name='admining_pk'),
    path('records/admining/delete/<str:username>', views.user_delete, name='user_delete'),
]


#url(r'^records/edit/(?P<records_id>\d+)/$', views.records, name='records_edit')
