from django import forms
from django.contrib.auth import get_user_model
from django.forms import NumberInput
from django.utils.translation import ugettext_lazy as _

from .models import Records, Records_ship

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
            'start_time': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18, 'value': 6}),
            'end_time': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18, 'value': 10}),
        }

    def clean(self):
        data = self.cleaned_data
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if start_time > end_time:
            raise forms.ValidationError('Введите корректное время поездки')
        if (end_time - start_time) > 8:
            raise forms.ValidationError('Нельзя кататься больше 8 часов')
        if (end_time - start_time) <= 1:
            raise forms.ValidationError('Нельзя кататься меньше 2 часов')
        return data


class Records_shipForm(forms.ModelForm):

    class Meta:
        model = Records_ship
        fields = ['start_time', 'end_time']
        labels = {
            'start_time': _('Время начала поездки'),
            'end_time': _('Время конца поездки'),
        }
        widgets = {
            'start_time': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18, 'value': 6},),
            'end_time': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18, 'value': 10}),
        }

    def clean(self):
        data = self.cleaned_data
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if start_time > end_time:
            raise forms.ValidationError('Введите корректное время поездки')
        if (end_time - start_time) > 8:
            raise forms.ValidationError('Нельзя кататься больше 8 часов')
        if (end_time - start_time) <= 1:
            raise forms.ValidationError('Нельзя кататься меньше 2 часов')
        return data


class long_recordsForm(forms.ModelForm):

    class Meta:
        model = Records
        fields = ['date_start', 'date_end', 'start_time', 'end_time']
        labels = {
            'date_start': _('День начала'),
            'date_end': _('День конца'),
            'start_time': _('Время начала поездки'),
            'end_time': _('Время конца поездки'),
        }
        widgets = {
            'start_time': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18, 'value': 6}),
            'end_time': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18, 'value': 10}),
        }
