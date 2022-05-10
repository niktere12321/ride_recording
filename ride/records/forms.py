from django import forms
from django.contrib.auth import get_user_model
from django.forms import NumberInput
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
            'start_time': NumberInput(attrs={'type': 'number'}),
            'end_time': NumberInput(attrs={'type': 'number'}),
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
            'contact': _('Человек ответственный за т.с.'),
        }

    def clean(self):
        data = self.cleaned_data
        low_time = data.get('low_time')
        high_time = data.get('high_time')
        if low_time >= high_time:
            raise forms.ValidationError('Разрешенное время начала катания не может быть больше конца')
        return data
