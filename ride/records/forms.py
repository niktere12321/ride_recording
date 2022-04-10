from django import forms
from django.contrib.auth import get_user_model
from django.forms import NumberInput
from django.utils.translation import ugettext_lazy as _

from .models import Records, Records_ship

User = get_user_model()


class RecordsForm(forms.ModelForm):

    class Meta:
        model = Records
        fields = ['start_int', 'end_int']
        labels = {
            'start_int': _('Время начала поездки'),
            'end_int': _('Время конца поездки'),
        }
        widgets = {
            'start_int': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18, 'value': 6}),
            'end_int': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18, 'value': 10}),
        }

    def clean(self):
        data = self.cleaned_data
        start_int = data.get('start_int')
        end_int = data.get('end_int')
        if start_int > end_int:
            raise forms.ValidationError('Введите корректное время поездки')
        if (end_int - start_int) > 8:
            raise forms.ValidationError('Нельзя кататься больше 8 часов')
        if (end_int - start_int) <= 1:
            raise forms.ValidationError('Нельзя кататься меньше 2 часов')
        return data


class Records_shipForm(forms.ModelForm):

    class Meta:
        model = Records_ship
        fields = ['start_int', 'end_int']
        labels = {
            'start_int': _('Время начала поездки'),
            'end_int': _('Время конца поездки'),
        }
        widgets = {
            'start_int': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18, 'value': 6},),
            'end_int': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18, 'value': 10}),
        }

    def clean(self):
        data = self.cleaned_data
        start_int = data.get('start_int')
        end_int = data.get('end_int')
        if start_int > end_int:
            raise forms.ValidationError('Введите корректное время поездки')
        if (end_int - start_int) > 8:
            raise forms.ValidationError('Нельзя кататься больше 8 часов')
        if (end_int - start_int) <= 1:
            raise forms.ValidationError('Нельзя кататься меньше 2 часов')
        return data
