from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RecordsForm
from .models import Records


@login_required
def index(request):
    records = Records.objects.all()
    context = {'records': records}
    return render(request, 'records/index.html', context)


@login_required
def records(request):
    form = RecordsForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'records/records.html', {'form': form})
    records = form.save(commit=False)
    records.driver = request.user
    records.save()
    return redirect('records:index')
