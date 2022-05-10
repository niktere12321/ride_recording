from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from ride.settings import DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL

from users.forms import Add_new_userForm, CreationForm

User = get_user_model()


def SignUp(request):
    form = CreationForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('records:index_services'))
    else:
        context = {'form': form}
        return render(request, 'users/signup.html', context)


@login_required
def add_new_user(request):
    if request.user.is_superuser:
        form = Add_new_userForm(request.POST or None)
        if request.POST and form.is_valid():
            from_email = form.cleaned_data['from_email']
            subject = 'Приглашение на регистрацию'
            message = 'Приглашаем пройти регистрацию на http://127.0.0.1:8000/users/signup/'
            try:
                send_mail(f'{subject} от {from_email}', message,
                          DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect(reverse('records:index_services'))
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, "email/email.html", {'form': form})
