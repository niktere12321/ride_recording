from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm, PhoneForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('users:phone')
    template_name = 'users/signup.html'


def phone(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            return redirect(reverse('records:index'))
    else:
        form = PhoneForm()
    return render(request, 'users/phone.html', {'form': form})
