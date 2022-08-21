from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from api.views import Get_week

app_name = 'api'

urlpatterns = [
    path('get_week/<int:date>/<int:project>', Get_week, name='Get_week'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
