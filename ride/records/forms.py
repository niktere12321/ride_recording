import datetime

from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.contrib.auth import get_user_model

from .models import Records

User = get_user_model()


class RecordsForm(forms.ModelForm):

    class Meta:
        model = Records
        fields = ['start_date', 'start_time', 'end_time', 'car_or_ship']

    def clean_start_date(self):
        data = self.cleaned_data['start_date']
        if data < datetime.date.today():
            raise forms.ValidationError('Надо выбрать другую дату')
        return data
    
    def clean_start_time(self):
        data = {'time': self.cleaned_data['start_time'], 'date': self.cleaned_data['start_date']}
        if data['date'] in Records.objects.filter(start_date=data['date']) and (Records.objects.filter(start_date=data['date'], start_time=data['time']) > data['time'] > Records.objects.filter(start_date=data['date'], start_time=data['time'])):
            raise forms.ValidationError('Надо выбрать другую дату')
        return data

