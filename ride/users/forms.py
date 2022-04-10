from django import forms
from django.contrib.auth import get_user_model
from django.forms import EmailInput, TextInput
from django.utils.translation import ugettext_lazy as _

from . import password_validations

User = get_user_model()


class CreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("Два поля пароля не совпадают."),
    }
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validations.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Подтвердите пароль"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Введите тот же пароль."),
    )

    class Meta:
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validations.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
