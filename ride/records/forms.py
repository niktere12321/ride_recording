from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Records

User = get_user_model()


class RecordsForm(ModelForm):

    class Meta:
        model = Records
        fields = ['start_date', 'end_date', 'car_or_ship']
