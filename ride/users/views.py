from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from users.forms import Add_new_userForm, CreationForm

User = get_user_model()


def SignUp(request, new_email):
    form = CreationForm(request.POST or None, initial={'email': new_email})
    if request.POST and form.is_valid():
        form.email = new_email
        form.save()
        return redirect(reverse('records:index_services'))
    else:
        context = {'form': form,
                   'new_email': new_email}
        return render(request, 'users/signup.html', context)


@login_required
def add_new_user(request):
    if request.user.is_superuser:
        form = Add_new_userForm(request.POST or None)
        if request.POST and form.is_valid():
            to_email = form.cleaned_data['to_email']
            if to_email.find(',') >= 1:
                email = to_email.split(',')
                for i in range(len(email)):
                    email_from = settings.EMAIL_HOST_USER
                    subject = 'Приглашение на регистрацию'
                    message = f'Приглашаем пройти регистрацию на http://127.0.0.1:8000/users/signup/{email[i]}/'
                    go_to_email = [email[i]]
                    try:
                        send_mail(subject, message, email_from, go_to_email)
                    except BadHeaderError:
                       return HttpResponse('Ошибка в теме письма.')
            else:
                email = [to_email]
                email_from = settings.EMAIL_HOST_USER
                subject = 'Приглашение на регистрацию'
                message = f'Приглашаем пройти регистрацию на http://127.0.0.1:8000/users/signup/{email}/'
                try:
                    send_mail(subject, message, email_from, email)
                except BadHeaderError:
                    return HttpResponse('Ошибка в теме письма.')
            return redirect(reverse('records:index_services'))
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, "email/email.html", {'form': form})
