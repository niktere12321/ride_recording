from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailInput, TextInput
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('Email адрес'),
            'username': _('Имя пользователя'),
        }
        widgets = {
            'first_name': TextInput(attrs={'type': 'text', 'required': True,}),
            'last_name': TextInput(attrs={'type': 'text', 'required': True}),
            'email': EmailInput(attrs={'type': 'email', 'required': True}),
        }
