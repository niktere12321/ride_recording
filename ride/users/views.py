from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from records.decorathion import active

from users.forms import Add_new_userForm, CreationForm, EditUserForm, HelpForm

User = get_user_model()


def SignUp(request, new_email):
    """Регистрация"""
    form = CreationForm(request.POST or None, initial={'email': new_email})
    if request.POST and form.is_valid():
        form.email = new_email
        form.save()
        return redirect(reverse('records:index_services'))
    else:
        context = {'form': form,
                   'new_email': new_email}
        return render(request, 'users/signup.html', context)


@active
@login_required
def edd_user(request, username):
    """Изменение данных пользователя"""
    user = get_object_or_404(User, username=username)
    form = EditUserForm(request.POST or None, instance=user)
    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('records:index_services'))
    else:
        context = {'form': form,
                   'username': username}
        return render(request, 'users/edd_user.html', context)


@active
@login_required
def add_new_user(request):
    """Приглашение на регистрацию"""
    if request.user.is_superuser:
        form = Add_new_userForm(request.POST or None)
        if request.POST and form.is_valid():
            to_email = form.cleaned_data['to_email']
            if to_email.find(',') >= 1:
                email = to_email.split(',')
                for i in range(len(email)):
                    email_from = settings.EMAIL_HOST_USER
                    subject = 'Приглашение на регистрацию'
                    message = f'Приглашаем пройти регистрацию на http://broniryu-itochka.ddns.net/users/signup/{email[i]}/'
                    go_to_email = [email[i]]
                    try:
                        send_mail(subject, message, email_from, go_to_email)
                    except BadHeaderError:
                       return HttpResponse('Ошибка в теме письма.')
            else:
                email = [to_email]
                email_from = settings.EMAIL_HOST_USER
                subject = 'Приглашение на регистрацию'
                message = f'Приглашаем пройти регистрацию на http://broniryu-itochka.ddns.net/users/signup/{email[0]}/'
                try:
                    send_mail(subject, message, email_from, email)
                except Exception as e:
                    return HttpResponse('Произошла ошибка.')
            return redirect(reverse('records:index_services'))
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, "email/email.html", {'form': form})


def help_active(request):
    """Страничка для заблокированных пользователей"""
    if request.user.active == False:
        return render(request, 'users/help_active.html')
    return redirect(reverse('records:index_services'))


def users_help(request):
    """Сообщение от пользователя"""
    if request.user.is_authenticated:
        form = HelpForm(request.POST or None)
        if request.POST and form.is_valid():
            subject = 'Сообщение об ошибке'
            message = form.cleaned_data['message']
            email = [request.user.email]
            email_from = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message, email_from, email)
            except Exception as e:
                return HttpResponse('Произошла ошибка.')
            return redirect(reverse('records:index_services'))
        return render(request, "users/users_help.html", {'form': form})
