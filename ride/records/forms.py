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

    def clean(self):
        data = self.cleaned_data
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        car = data.get('car_or_ship')
        start_list = []
        end_list = []
        lol = []
        queryset_list = list(Records.objects.filter(car_or_ship=car))
        for i in range(0, len(queryset_list)):
            lol.append(queryset_list[i].pk)
        for i in range(0, len(lol)):
            start_list.append(Records.objects.get(pk=lol[i]).start_time)
            end_list.append(Records.objects.get(pk=lol[i]).end_time)
        if start_time.timestamp() < datetime.datetime.now().timestamp():
            raise forms.ValidationError('Нельзя записаться в прошлом времени !')
        if end_time.timestamp() < start_time.timestamp():
            raise forms.ValidationError('Нельзя путешествовать во времени !')
        if (end_time.timestamp() - start_time.timestamp()) >= 10800:
            raise forms.ValidationError('Поездка не должна занимать больше 3 часов !')
        for i in start_list:
            for p in end_list:
                if i.timestamp() <= start_time.timestamp() and p.timestamp() >= start_time.timestamp():
                    raise forms.ValidationError('В это время уже катается другой')
        return data

    def __init__(self, *args, **kwargs):
        super(RecordsForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
