from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'records'


urlpatterns = [
    path('', views.index_services, name='index_services'),
    path(r'<int:project>', views.CalendarView.as_view(), name='index_records'),
    url(r'(?P<project>[0-9])/records/(?P<date>[0-9]{8})/$', views.records_start, name='records_start'),
    path('records/records/<int:rec_pk>/delete/<int:project>/<int:date>/', views.records_delete, name='records_delete'),
    path('records/records/<int:rec_pk>/delete/<str:prof>', views.records_delete_prof, name='records_delete_prof'),
    path('records/profiles', views.profiles, name='profiles'),
    path('records/admining', views.admining, name='admining'),
    path('records/services/<int:service_id>', views.admining_services, name='admining_services'),
    path('records/services/create', views.admining_services_create, name='admining_services_create'),
    path('records/services/edit/<int:services_id>', views.admining_services_edit, name='admining_services_edit'),
    path('records/admining/users', views.admining_users, name='admining_users'),
    path('records/admining/<str:username>', views.admining_pk, name='admining_pk'),
    path('records/admining/delete/<str:username>', views.user_delete, name='user_delete'),
    path('records/admining/services/<int:services_id>', views.admining_services_del, name='admining_services_del'),
    path('records/admining_statistics/<str:pass_date>/<str:future_date>', views.admining_statistics, name='admining_statistics'),
    path('records/admining/user_pass_or_active/<str:username>', views.user_pass_or_active, name='user_pass_or_active'),
]
