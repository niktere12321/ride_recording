from datetime import datetime

from django.utils.safestring import mark_safe
from records.models import Services
from records.utils import get_week_card
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def Next_week(request, date, project):
    if date is not None and project is not None:
        services = Services.objects.get(pk=project)
        new_date = str(date)[:4] + '-' + str(date)[4:6] + '-' + str(date)[6:]
        date_record = datetime.strptime(new_date, '%Y-%m-%d').date()
        week_line = get_week_card(date_record, services, new_date, project)
        return Response({'week_line': f'{mark_safe(week_line)}'})
    return Response({'error': 'Произошла ошибка!'})


@api_view(['GET'])
def Prev_week(request, date, project):
    if date is not None and project is not None:
        services = Services.objects.get(pk=project)
        new_date = str(date)[:4] + '-' + str(date)[4:6] + '-' + str(date)[6:]
        date_record = datetime.strptime(new_date, '%Y-%m-%d').date()
        week_line = get_week_card(date_record, services, new_date, project)
        return Response({'week_line': f'{mark_safe(week_line)}'})
    return Response({'error': 'Произошла ошибка!'})
