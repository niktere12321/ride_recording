import calendar
from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic

from .forms import RecordsForm
from .models import Records
from .utils import Calendar


class CalendarView(generic.ListView):
    model = Records
    template_name = 'records/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required
def records(request, records_id=None):
    instance = Records()
    if records_id:
        instance = get_object_or_404(Records, pk=records_id)
    else:
        instance = Records()
    form = RecordsForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        records = form.save(commit=False)
        records.driver = request.user
        records.save()
        return HttpResponseRedirect(reverse('records:index'))
    return render(request, 'records/records.html', {'form': form})
