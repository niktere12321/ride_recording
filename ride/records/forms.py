import re
from datetime import date, datetime
from tracemalloc import start

from django import forms
from django.contrib.auth import get_user_model
from django.forms import TimeInput
from django.utils.translation import ugettext_lazy as _

from .models import Records, Services
from .utils import convert_time

User = get_user_model()


class RecordsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.new_date = kwargs.pop('date_to_validate', None)
        self.project = kwargs.pop('project_to_validate', None)
        super(RecordsForm, self).__init__(*args,**kwargs)
        
    class Meta:
        model = Records
        fields = ['start_time', 'end_time']
        labels = {
            'start_time': _('Время начала поездки'),
            'end_time': _('Время конца поездки'),
        }
        widgets = {
            'start_time': TimeInput(attrs={'type': 'text', 'readonly': 'readonly'}),
            'end_time': TimeInput(attrs={'type': 'text', 'readonly': 'readonly'}),
        }

    def clean(self):
        data = self.cleaned_data
        start_ti = data.get('start_time')
        end_ti = data.get('end_time')
        regex = r"^\d{2}:\d{2}:00$"
        if re.search(regex, str(start_ti)) is None or re.search(regex, str(end_ti)) is None:
            raise forms.ValidationError("Время должно быть в формате: 20:00")
        services = Services.objects.get(pk=self.project)
        record_list_p = list(Records.objects.filter(date_start=self.new_date))
        record_list = list(Records.objects.filter(date_start=self.new_date, project=self.project))
        date_record = datetime.strptime(self.new_date, '%Y-%m-%d').date()
        convert_end_time = convert_time(end_ti)
        convert_start_time = convert_time(start_ti)
        if date_record == datetime.now().date():
            if datetime.strptime(f"{start_ti}", "%H:%M:%S").time() < datetime.now().time():
                raise forms.ValidationError("Нельзя записаться в прошлом.")
        if start_ti > end_ti:
            raise forms.ValidationError("Введите корректное время поездки.")
        if convert_end_time - convert_start_time > convert_time(f'{services.high_duration}:00:00'):
            raise forms.ValidationError(f"Нельзя кататься больше {services.high_duration} часов")
        if (convert_end_time - convert_start_time) <= convert_time(f'{services.low_duration}:00:00'):
            raise forms.ValidationError(f"Нельзя кататься меньше {services.low_duration} часов")
        if convert_end_time > convert_time(f'{services.high_time}:00:00'):
            raise forms.ValidationError(f"Нельзя кататься после {services.high_time} часов")
        if convert_start_time < convert_time(f'{services.low_time}:00:00'):
            raise forms.ValidationError(f"Нельзя кататься раньше {services.low_time} часов")
        record_st = []
        record_en = []
        for i in range(0, len(record_list)):
            record_st.append(record_list[i].start_time)
            record_en.append(record_list[i].end_time)
        for i in range(len(record_st)):
            if (start_ti >= record_st[i] and end_ti <= record_en[i]) or (start_ti > record_st[i] and start_ti < record_en[i] and end_ti > record_en[i]):
                raise forms.ValidationError("Это время уже занято!")
            elif start_ti <= record_st[i] and end_ti >= record_en[i]:
                raise forms.ValidationError("Это время уже занято!")
            elif start_ti < record_st[i] and end_ti <= record_st[i]:
                continue
            elif start_ti < record_st[i] and end_ti <= record_en[i]:
                raise forms.ValidationError("Это время уже занято!")
        record_st_p = []
        record_en_p = []
        for i in range(0, len(record_list_p)):
            record_st_p.append(record_list_p[i].start_time)
            record_en_p.append(record_list_p[i].end_time)
        for i in range(len(record_st)):
            if (start_ti >= record_st[i] and end_ti <= record_en[i]) or (start_ti > record_st[i] and start_ti < record_en[i] and end_ti > record_en[i]):
                raise forms.ValidationError("В это время вы уже катаетесь на другом т.с.")
            elif start_ti <= record_st[i] and end_ti >= record_en[i]:
                raise forms.ValidationError("В это время вы уже катаетесь на другом т.с.")
            elif start_ti < record_st[i] and end_ti <= record_st[i]:
                continue
            elif start_ti < record_st[i] and end_ti <= record_en[i]:
                raise forms.ValidationError("В это время вы уже катаетесь на другом т.с.")
        return data


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
