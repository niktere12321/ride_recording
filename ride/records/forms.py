from django import forms
from django.contrib.auth import get_user_model
from django.forms import EmailInput, NumberInput, TextInput, TimeInput
from django.utils.translation import ugettext_lazy as _

from .models import Records, Services

User = get_user_model()


class RecordsForm(forms.ModelForm):

    class Meta:
        model = Records
        fields = ['start_time', 'end_time']
        labels = {
            'start_time': _('Время начала поездки'),
            'end_time': _('Время конца поездки'),
        }
        widgets = {
            'start_time': TimeInput(attrs={'type': 'text'}),
            'end_time': TimeInput(attrs={'type': 'text'}),
        }


class ServicesForm(forms.ModelForm):

    class Meta:
        model = Services
        fields = '__all__'
        labels = {
            'name_project': _('Название транспортного сретства'),
            'description': _('Описание'),
            'low_time': _('Разрешенное время начала поездки'),
            'high_time': _('Разрешенное время конца поездки'),
            'low_duration': _('Минимальная длительность поездки'),
            'high_duration': _('Максимальная длительность поездки'),
            'image': _('Изображение'),
            'contact': _('Помощь человеку в поездке.'),
        }
        widgets = {
            'low_time': TimeInput(attrs={'type': 'text', 'value': '00:00'}),
            'high_time': TimeInput(attrs={'type': 'text', 'value': '23:55'}),
            'low_duration': TimeInput(attrs={'type': 'text', 'value': '00:00'}),
            'high_duration': TimeInput(attrs={'type': 'text', 'value': '23:55'}),
        }

    def clean(self):
        data = self.cleaned_data
        low_time = data.get('low_time')
        high_time = data.get('high_time')
        low_duration = data.get('low_duration')
        high_duration = data.get('high_duration')
        if low_time == None or high_time == None or low_duration == None or high_duration == None:
            raise forms.ValidationError('Введите корректное время')
        if low_time >= high_time:
            raise forms.ValidationError('Разрешенное время начала катания не может быть больше конца')
        return data
