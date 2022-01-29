import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.forms import DateInput

from .models import Records

User = get_user_model()


class RecordsForm(forms.ModelForm):

    class Meta:
        model = Records
        fields = ['start_time', 'end_time', 'car_or_ship']
        widgets = {
        'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ['start_time', 'end_time', 'car_or_ship']
    
    def __init__(self, *args, **kwargs):
        super(RecordsForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

    def clean_start_date(self):
        data = self.cleaned_data['start_date']
        if data < datetime.date.today():
            raise forms.ValidationError('Надо выбрать другую дату')
        return data
