from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from api.views import Next_week, Prev_week

app_name = 'api'

urlpatterns = [
    path('next_week/<int:date>/<int:project>', Next_week, name='Next_week'),
    path('prev_week/<int:date>/<int:project>', Prev_week, name='Prev_week'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
