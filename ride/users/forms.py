from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailInput, TextInput
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class CreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone',)
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('Email адрес'),
            'username': _('Имя пользователя'),
            'phone': _('Телефон')
        }
        widgets = {
            'first_name': TextInput(attrs={'type': 'text', 'required': True,}),
            'last_name': TextInput(attrs={'type': 'text', 'required': True}),
            'email': EmailInput(attrs={'type': 'email', 'required': True}),
        }


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone',)
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('Email адрес'),
            'username': _('Имя пользователя'),
            'phone': _('Телефон')
        }
        widgets = {
            'first_name': TextInput(attrs={'type': 'text', 'required': True,}),
            'last_name': TextInput(attrs={'type': 'text', 'required': True}),
            'email': EmailInput(attrs={'type': 'email', 'required': True}),
        }


class Add_new_userForm(forms.Form):
    to_email = forms.CharField(label='Введите email новых пользователей(я)', widget=forms.Textarea(attrs={'cols': 50, 'rows': 1, 'required': True, 'placeholder': 'email1@email1.email1,email2@email1.email1'}))


class HelpForm(forms.Form):
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 30, 'rows': 5, 'type': 'text', 'required': True,}))
