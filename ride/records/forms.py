import datetime

from dateutil.parser import parse
from django import forms
from django.contrib.auth import get_user_model
from django.forms import DateInput

from .models import Records

User = get_user_model()


class RecordsForm(forms.ModelForm):

    class Meta:
        model = Records
        fields = ['start_time', 'end_time', 'car_or_ship']
        widgets = {'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), 'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),}

    def clean(self):
        data = self.cleaned_data
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if start_time.timestamp() < datetime.datetime.now().timestamp():
            raise forms.ValidationError('Нельзя записаться в прошлом времени !')
        if end_time.timestamp() < start_time.timestamp():
            raise forms.ValidationError('Нельзя путешествовать во времени !')
        if (end_time.timestamp() - start_time.timestamp()) >= 10800:
            raise forms.ValidationError('Поездка не должна занимать больше 3 часов !')
        return data

    def __init__(self, *args, **kwargs):
        super(RecordsForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
