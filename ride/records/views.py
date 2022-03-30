import calendar
from datetime import date, datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic

from .forms import Records_shipForm, RecordsForm
from .models import Records, Records_ship
from .utils import Calendar, Calendar_ship

User = get_user_model()


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


class Calendar_shipView(generic.ListView):
    model = Records_ship
    template_name = 'records/index_ship.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal_ship = Calendar_ship(d.year, d.month)
        html_cal = cal_ship.formatmonth(withyear=True)
        context['calendar_ship'] = mark_safe(html_cal)
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
def records_start(request, date):
    new_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
    record_list = list(Records.objects.filter(date_start=new_date))
    record_st = []
    record_en = []
    for i in range(0, len(record_list)):
        record_st.append(record_list[i].start_time)
        record_en.append(record_list[i].end_time)
    pk_user = User.objects.get(username=request.user.username).id
    about_count = Records.objects.filter(driver=pk_user).filter(date_start__gt=datetime.now()).count()
    if about_count == 5:
        return render(request, 'records/records_start.html', context={"error": "Максимум записей 5", 'record_st': record_st, 'record_en': record_en})
    form = RecordsForm(request.POST or None)
    if request.POST and form.is_valid() and (datetime.strptime(new_date, '%Y-%m-%d') > datetime.now()):
        records = form.save(commit=False)
        records.date_start = new_date
        records.driver = request.user
        start_ti = form.cleaned_data['start_time']
        end_ti = form.cleaned_data['end_time']
        for i in record_st:
            for p in record_en:
                if (start_ti >= i and end_ti <= p) or (start_ti >= i and start_ti <= p and end_ti >= p):
                    return render(request, 'records/records_start.html', context={"error": "Нельзя кататься когаться когда уже катается!", 'record_st': record_st, 'record_en': record_en})
                elif start_ti <= i and end_ti <= p:
                    return render(request, 'records/records_start.html', context={"error": "Нельзя кататься когаться когда уже катается!", 'record_st': record_st, 'record_en': record_en})
        records.start_time = start_ti
        records.end_time = end_ti
        records.save()
        return redirect(reverse('records:index'))
    context = {'record_st': record_st,
                'record_en': record_en,
                'form': form}
    return render(request, 'records/records_start.html', context)


@login_required
def records_ship_start(request, date):
    new_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
    record_list = list(Records_ship.objects.filter(date_start=new_date))
    record_st = []
    record_en = []
    for i in range(0, len(record_list)):
        record_st.append(record_list[i].start_time)
        record_en.append(record_list[i].end_time)
    pk_user = User.objects.get(username=request.user.username).id
    about_count = Records_ship.objects.filter(driver=pk_user).filter(date_start__gt=datetime.now()).count()
    if about_count == 5:
        return render(request, 'records/records_start.html', context={"error": "Максимум записей 5", 'record_st': record_st, 'record_en': record_en})
    form = Records_shipForm(request.POST or None)
    if request.POST and form.is_valid() and (datetime.strptime(new_date, '%Y-%m-%d') > datetime.now()):
        records_ship = form.save(commit=False)
        records_ship.date_start = new_date
        records_ship.driver = request.user
        start_ti = form.cleaned_data['start_time']
        end_ti = form.cleaned_data['end_time']
        for i in record_st:
            for p in record_en:
                if (start_ti >= i and end_ti <= p) or (start_ti >= i and start_ti <= p and end_ti >= p):
                    return render(request, 'records/records_start.html', context={"error": "Нельзя кататься когаться когда другой катается!", 'record_st': record_st, 'record_en': record_en})
                elif start_ti <= i and end_ti <= p:
                    return render(request, 'records/records_start.html', context={"error": "Нельзя кататься когаться когда другой катается!", 'record_st': record_st, 'record_en': record_en})
        records_ship.start_time = start_ti
        records_ship.end_time = end_ti
        records_ship.save()
        return redirect(reverse('records:index_ship'))
    context = {'record_st': record_st,
                'record_en': record_en,
                'form': form}
    return render(request, 'records/records_start.html', context)


@login_required
def profiles(request):
    user = request.user
    prof = get_object_or_404(User, pk=user.pk)
    context = {'prof': prof}
    return render(request, 'records/profiles.html', context)
