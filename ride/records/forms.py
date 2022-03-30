from django import forms
from django.contrib.auth import get_user_model
from django.forms import NumberInput

from .models import Records, Records_ship

User = get_user_model()


class RecordsForm(forms.ModelForm):

    class Meta:
        model = Records
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18}),
            'end_time': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18}),
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
        widgets = {
            'start_time': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18}),
            'end_time': NumberInput(attrs={'type': 'number', 'min': 6, 'max': 18}),
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
