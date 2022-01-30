from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

valid_phone = ['89507638930', '89065864030', '89601043035', '89081357407', '89204283805', '89507669839', '89515450161', '89805525214']


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=11)

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if data not in valid_phone:
            raise forms.ValidationError('Введите коректный номер')
        return data
