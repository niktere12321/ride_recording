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
    new_date_str = date[6:] + '.' + date[4:6] + '.' + date[:4]
    record_list = Records.objects.filter(date_start=new_date)
    lol_red = f"<span style='outline: 2px solid #000; font-size: 18px; color: red; background-color: red'> ------- </span>"
    lol_green = f"<span style='outline: 2px solid #000; font-size: 18px; color: green; background-color: green'> ------- </span>"
    a1 = lol_green
    a2 = lol_green
    a3 = lol_green
    a4 = lol_green
    b1 = lol_green
    b2 = lol_green
    b3 = lol_green
    b4 = lol_green
    c1 = lol_green
    c2 = lol_green
    c3 = lol_green
    c4 = lol_green
    for event in record_list:
        for i in range(6, 19):
            if i == 6 and i >= event.start_time and i < event.end_time:
                a1 = lol_red
            elif i == 7 and i >= event.start_time and i < event.end_time:
                a2 = lol_red
            elif i == 8 and i >= event.start_time and i < event.end_time:
                a3 = lol_red
            elif i == 9 and i >= event.start_time and i < event.end_time:
                a4 = lol_red
            elif i == 10 and i >= event.start_time and i < event.end_time:
                b1 = lol_red
            elif i == 11 and i >= event.start_time and i < event.end_time:
                b2 = lol_red
            elif i == 12 and i >= event.start_time and i < event.end_time:
                b3 = lol_red
            elif i == 13 and i >= event.start_time and i < event.end_time:
                b4 = lol_red
            elif i == 14 and i >= event.start_time and i < event.end_time:
                c1 = lol_red
            elif i == 15 and i >= event.start_time and i < event.end_time:
                c2 = lol_red
            elif i == 16 and i >= event.start_time and i < event.end_time:
                c3 = lol_red
            elif i == 17 and i >= event.start_time and i < event.end_time:
                c4 = lol_red
    line_1 = f"{a1}{a2}{a3}{a4}"
    line_2 = f"{b1}{b2}{b3}{b4}"
    line_3 = f"{c1}{c2}{c3}{c4}"
    color_table = f"<div style='height: 100px; margin-left: 5%; margin-top: 3%;'><span>{line_1}</span><span>{line_2}</span><span>{line_3}</span></div>"
    record_list = list(Records.objects.filter(date_start=new_date))
    record_st = []
    record_en = []
    record_dri = []
    record_pk = []
    for i in range(0, len(record_list)):
        record_st.append(record_list[i].start_time)
        record_en.append(record_list[i].end_time)
        record_dri.append(record_list[i].driver)
        record_pk.append(record_list[i].pk)
    ride_rec = ''
    color_text = "style='font-size: 16px;'"
    for i in range(0, len(record_st)):
        if (i % 3) == 0 and i != 0:
            ride_rec += f"<span {color_text}>{record_dri[i]}:</span><span {color_text}> Время с {record_st[i]}</span><span {color_text}> до {record_en[i]}</span><br>"
        else:
            ride_rec += f"<span {color_text}>{record_dri[i]}:</span><span {color_text}> Время с {record_st[i]}</span><span {color_text}> до {record_en[i]};  </span>"
    ride_rec_adm = ''
    for i in range(0, len(record_st)):
        if (i % 3) == 0 and i != 0:
            ride_rec_adm += f"<span {color_text}>{record_dri[i]}:</span><span {color_text}> Время с {record_st[i]}</span><span {color_text}> до {record_en[i]}<a href='../records/{record_pk[i]}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a></span><br>"
        else:
            ride_rec_adm += f"<span {color_text}>{record_dri[i]}:</span><span {color_text}> Время с {record_st[i]}</span><span {color_text}> до {record_en[i]};  <a href='../records/{record_pk[i]}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a></span>"
    month_ride = int(date[4:6])
    d = get_date(request.GET.get('month', None))
    cal = Calendar(d.year, month_ride)
    html_cal = cal.formatmonth(withyear=True)
    if datetime.strptime(new_date, '%Y-%m-%d') <= datetime.now():
        context = {'ride_rec_adm': ride_rec_adm,
                   'ride_rec': ride_rec,
                   'color_table': color_table,
                   'calendar': mark_safe(html_cal),
                   'date_str': new_date_str,
                   'date': date,
                   'old_date': "Нельзя записаться в прошлом !"}
        return render(request, 'records/records_start.html', context)
    pk_user = User.objects.get(username=request.user.username).id
    about_count = Records.objects.filter(driver=pk_user).filter(date_start__gt=datetime.now()).count()
    if about_count == 10:
        context = {'ride_rec_adm': ride_rec_adm,
                   'ride_rec': ride_rec,
                   'color_table': color_table,
                   'calendar': mark_safe(html_cal),
                   'date_str': new_date_str,
                   'date': date,
                   'many_rec': "Максимум записей 10"}
        return render(request, 'records/records_start.html', context)
    form = RecordsForm(request.POST or None)
    if request.POST and form.is_valid() and (datetime.strptime(new_date, '%Y-%m-%d') > datetime.now()):
        records = form.save(commit=False)
        records.date_start = new_date
        records.driver = request.user
        start_ti = form.cleaned_data['start_time']
        end_ti = form.cleaned_data['end_time']
        for i in record_st:
            for p in record_en:
                if (start_ti >= i and end_ti <= p) or (start_ti > i and start_ti < p and end_ti > p):
                    return render(request, 'records/records_start.html', context={"error": "Это время уже занято!", "date": date})
                elif start_ti < i and end_ti <= i:
                    break
                elif start_ti < i and end_ti < p:
                    return render(request, 'records/records_start.html', context={"error": "Это время уже занято!", "date": date})
        records.start_time = start_ti
        records.end_time = end_ti
        records.save()
        return redirect(reverse('records:index'))
    context = {'ride_rec_adm': ride_rec_adm,
               'ride_rec': ride_rec,
               'color_table': color_table,
               'form': form,
               'calendar': mark_safe(html_cal),
               'date_str': new_date_str,
               'date': date}
    return render(request, 'records/records_start.html', context)

@login_required
def records_ship_start(request, date):
    new_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
    new_date_str = date[6:] + '.' + date[4:6] + '.' + date[:4]
    record_list = Records_ship.objects.filter(date_start=new_date)
    lol_red = f"<span style='outline: 2px solid #000; font-size: 18px; color: red; background-color: red'> ------- </span>"
    lol_green = f"<span style='outline: 2px solid #000; font-size: 18px; color: green; background-color: green'> ------- </span>"
    a1 = lol_green
    a2 = lol_green
    a3 = lol_green
    a4 = lol_green
    b1 = lol_green
    b2 = lol_green
    b3 = lol_green
    b4 = lol_green
    c1 = lol_green
    c2 = lol_green
    c3 = lol_green
    c4 = lol_green
    for event in record_list:
        for i in range(6, 19):
            if i == 6 and i >= event.start_time and i < event.end_time:
                a1 = lol_red
            elif i == 7 and i >= event.start_time and i < event.end_time:
                a2 = lol_red
            elif i == 8 and i >= event.start_time and i < event.end_time:
                a3 = lol_red
            elif i == 9 and i >= event.start_time and i < event.end_time:
                a4 = lol_red
            elif i == 10 and i >= event.start_time and i < event.end_time:
                b1 = lol_red
            elif i == 11 and i >= event.start_time and i < event.end_time:
                b2 = lol_red
            elif i == 12 and i >= event.start_time and i < event.end_time:
                b3 = lol_red
            elif i == 13 and i >= event.start_time and i < event.end_time:
                b4 = lol_red
            elif i == 14 and i >= event.start_time and i < event.end_time:
                c1 = lol_red
            elif i == 15 and i >= event.start_time and i < event.end_time:
                c2 = lol_red
            elif i == 16 and i >= event.start_time and i < event.end_time:
                c3 = lol_red
            elif i == 17 and i >= event.start_time and i < event.end_time:
                c4 = lol_red
    line_1 = f"{a1}{a2}{a3}{a4}"
    line_2 = f"{b1}{b2}{b3}{b4}"
    line_3 = f"{c1}{c2}{c3}{c4}"
    color_table = f"<div style='height: 100px; margin-left: 5%; margin-top: 3%;'><span>{line_1}</span><span>{line_2}</span><span>{line_3}</span></div>"
    record_list = list(Records_ship.objects.filter(date_start=new_date))
    record_st = []
    record_en = []
    record_dri = []
    record_pk = []
    for i in range(0, len(record_list)):
        record_st.append(record_list[i].start_time)
        record_en.append(record_list[i].end_time)
        record_dri.append(record_list[i].driver)
    ride_rec = ''
    color_text = "style='font-size: 16px;'"
    for i in range(0, len(record_st)):
        if (i % 3) == 0 and i != 0:
            ride_rec += f"<span {color_text}>{record_dri[i]}:</span><span {color_text}> Время с {record_st[i]}</span><span {color_text}> до {record_en[i]}</span><br>"
        else:
            ride_rec += f"<span {color_text}>{record_dri[i]}:</span><span {color_text}> Время с {record_st[i]}</span><span {color_text}> до {record_en[i]};  </span>"
    ride_rec_adm = ''
    for i in range(0, len(record_pk)):
        if (i % 3) == 0 and i != 0:
            ride_rec_adm += f"<span {color_text}>{record_dri[i]}:</span><span {color_text}> Время с {record_st[i]}</span><span {color_text}> до {record_en[i]}<a href='../records/{record_pk[i]}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a></span><br>"
        else:
            ride_rec_adm += f"<span {color_text}>{record_dri[i]}:</span><span {color_text}> Время с {record_st[i]}</span><span {color_text}> до {record_en[i]};  <a href='../records/{record_pk[i]}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a></span>"
    month_ride = int(date[4:6])
    d = get_date(request.GET.get('month', None))
    cal_ship = Calendar_ship(d.year, month_ride)
    html_cal_ship = cal_ship.formatmonth(withyear=True)
    if datetime.strptime(new_date, '%Y-%m-%d') <= datetime.now():
        context = {'ride_rec_adm': ride_rec_adm,
                   'ride_rec': ride_rec,
                   'color_table': color_table,
                   'calendar_ship': mark_safe(html_cal_ship),
                   'date_str': new_date_str,
                   'date': date,
                   'old_date': "Нельзя записаться в прошлом !"}
        return render(request, 'records/records_ship_start.html', context)
    pk_user = User.objects.get(username=request.user.username).id
    about_count = Records_ship.objects.filter(driver=pk_user).filter(date_start__gt=datetime.now()).count()
    if about_count == 10:
        context = {'ride_rec_adm': ride_rec_adm,
                   'ride_rec': ride_rec,
                   'color_table': color_table,
                   'calendar_ship': mark_safe(html_cal_ship),
                   'date_str': new_date_str,
                   'date': date,
                   'many_rec': "Максимум записей 10"}
        return render(request, 'records/records_ship_start.html', context)
    form = Records_shipForm(request.POST or None)
    if request.POST and form.is_valid() and (datetime.strptime(new_date, '%Y-%m-%d') > datetime.now()):
        records_ship = form.save(commit=False)
        records_ship.date_start = new_date
        records_ship.driver = request.user
        start_ti = form.cleaned_data['start_time']
        end_ti = form.cleaned_data['end_time']
        for i in record_st:
            for p in record_en:
                if (start_ti >= i and end_ti <= p) or (start_ti > i and start_ti < p and end_ti > p):
                    return render(request, 'records/records_ship_start.html', context={"error": "Это время уже занято!", "date": date})
                elif start_ti < i and end_ti <= i:
                    break
                elif start_ti < i and end_ti < p:
                    return render(request, 'records/records_ship_start.html', context={"error": "Это время уже занято!", "date": date})
        records_ship.start_time = start_ti
        records_ship.end_time = end_ti
        records_ship.save()
        return redirect(reverse('records:index_ship'))
    context = {'ride_rec_adm': ride_rec_adm,
               'ride_rec': ride_rec,
               'color_table': color_table,
               'form': form,
               'calendar_ship': mark_safe(html_cal_ship),
               'date_str': new_date_str,
               'date': date}
    return render(request, 'records/records_ship_start.html', context)


@login_required
def profiles(request):
    user = User.objects.get(username=request.user.username)
    prof_email = user.email
    prof_firstname = user.first_name
    prof_lastname = user.last_name
    rec_user_new = list(Records.objects.filter(driver=user.pk).filter(date_start__gt=datetime.now()))
    record_date = []
    record_st = []
    record_en = []
    records_pk = []
    html_rec_user_new = f""
    for i in range(0, len(rec_user_new)):
        record_date.append(rec_user_new[i].date_start)
        record_st.append(rec_user_new[i].start_time)
        record_en.append(rec_user_new[i].end_time)
        records_pk.append(rec_user_new[i].pk)
    for i in range(0, len(record_st)):
        html_rec_user_new += f"<span style='font-size: 18px;'>{prof_lastname} {prof_firstname}: {record_date[i]}:{record_st[i]}-{record_en[i]}<a href='records/{records_pk[i]}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a></span><br>"
    rec_user_old = list(Records.objects.filter(driver=user.pk).filter(date_start__lte=datetime.now()))
    record_date_old = []
    record_st_old = []
    record_en_old = []
    records_pk_old = []
    html_rec_user_old = f""
    for i in range(0, len(rec_user_old)):
        record_date_old.append(rec_user_old[i].date_start)
        record_st_old.append(rec_user_old[i].start_time)
        record_en_old.append(rec_user_old[i].end_time)
        records_pk_old.append(rec_user_old[i].pk)
    for i in range(0, len(record_st_old)):
        html_rec_user_old += f"<span style='font-size: 18px;'>{prof_lastname} {prof_firstname}: {record_date_old[i]}:{record_st_old[i]}-{record_en_old[i]}</span><br>"
    rec_user_old_ship = list(Records_ship.objects.filter(driver=user.pk).filter(date_start__lte=datetime.now()))
    record_date_old_ship = []
    record_st_old_ship = []
    record_en_old_ship = []
    records_pk_old_ship = []
    html_rec_user_old_ship = f""
    for i in range(0, len(rec_user_old_ship)):
        record_date_old_ship.append(rec_user_old_ship[i].date_start)
        record_st_old_ship.append(rec_user_old_ship[i].start_time)
        record_en_old_ship.append(rec_user_old_ship[i].end_time)
        records_pk_old_ship.append(rec_user_old_ship[i].pk)
    for i in range(0, len(record_st_old_ship)):
        html_rec_user_old_ship += f"<span style='font-size: 18px;'>{prof_lastname} {prof_firstname}: {record_date_old_ship[i]}:{record_st_old_ship[i]}-{record_en_old_ship[i]}</span><br>"
    rec_user_new_ship = list(Records_ship.objects.filter(driver=user.pk).filter(date_start__gt=datetime.now()))
    record_date_ship = []
    record_st_ship = []
    record_en_ship = []
    records_pk_ship = []
    html_rec_user_new_ship = f""
    for i in range(0, len(rec_user_new_ship)):
        record_date_ship.append(rec_user_new_ship[i].date_start)
        record_st_ship.append(rec_user_new_ship[i].start_time)
        record_en_ship.append(rec_user_new_ship[i].end_time)
        records_pk_ship.append(rec_user_new_ship[i].pk)
    for i in range(0, len(record_st_ship)):
        html_rec_user_new_ship += f"<span style='font-size: 18px;'>{prof_lastname} {prof_firstname}: {record_date_ship[i]}:{record_st_ship[i]}-{record_en_ship[i]}<a href='records/{records_pk_ship[i]}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a></span><br>"
    context = {'html_rec_user_old': html_rec_user_old,
               'html_rec_user_old_ship': html_rec_user_old_ship,
               'html_rec_user_new': html_rec_user_new,
               'html_rec_user_new_ship': html_rec_user_new_ship,
               'prof': user,
               'prof_email': prof_email,
               'prof_firstname': prof_firstname,
               'prof_lastname': prof_lastname,}
    return render(request, 'records/profiles.html', context)


@login_required
def records_delete(request, rec_pk):
    records_del = get_object_or_404(Records, pk=rec_pk)
    if request.user == records_del.driver:
        records_del.delete()
        return render(request, 'records/delete.html', context={'messages': 'Вы успешно удалили запись'})
    return render(request, 'records/index.html', context={'messages': 'У вас нету прав'})


@login_required
def admining_pk(request, username):
    if request.user.is_superuser:
        user = get_object_or_404(User, username=username)
        prof = user
        prof_email = user.email
        prof_firstname = user.first_name
        prof_lastname = user.last_name
        rec_user_new = list(Records.objects.filter(driver=user.pk).filter(date_start__gt=datetime.now()))
        record_date = []
        record_st = []
        record_en = []
        records_pk = []
        html_rec_user_new = f""
        for i in range(0, len(rec_user_new)):
            record_date.append(rec_user_new[i].date_start)
            record_st.append(rec_user_new[i].start_time)
            record_en.append(rec_user_new[i].end_time)
            records_pk.append(rec_user_new[i].pk)
        for i in range(0, len(record_st)):
            html_rec_user_new += f"<span style='font-size: 18px;'>{prof_lastname} {prof_firstname}: {record_date[i]}:{record_st[i]}-{record_en[i]}<a href='records/{records_pk[i]}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a></span><br>"
        rec_user_old = list(Records.objects.filter(driver=user.pk).filter(date_start__lte=datetime.now()))
        record_date_old = []
        record_st_old = []
        record_en_old = []
        records_pk_old = []
        html_rec_user_old = f""
        for i in range(0, len(rec_user_old)):
            record_date_old.append(rec_user_old[i].date_start)
            record_st_old.append(rec_user_old[i].start_time)
            record_en_old.append(rec_user_old[i].end_time)
            records_pk_old.append(rec_user_old[i].pk)
        for i in range(0, len(record_st_old)):
            html_rec_user_old += f"<span style='font-size: 18px;'>{prof_lastname} {prof_firstname}: {record_date_old[i]}:{record_st_old[i]}-{record_en_old[i]}</span><br>"
        rec_user_old_ship = list(Records_ship.objects.filter(driver=user.pk).filter(date_start__lte=datetime.now()))
        record_date_old_ship = []
        record_st_old_ship = []
        record_en_old_ship = []
        records_pk_old_ship = []
        html_rec_user_old_ship = f""
        for i in range(0, len(rec_user_old_ship)):
            record_date_old_ship.append(rec_user_old_ship[i].date_start)
            record_st_old_ship.append(rec_user_old_ship[i].start_time)
            record_en_old_ship.append(rec_user_old_ship[i].end_time)
            records_pk_old_ship.append(rec_user_old_ship[i].pk)
        for i in range(0, len(record_st_old_ship)):
            html_rec_user_old_ship += f"<span style='font-size: 18px;'>{prof_lastname} {prof_firstname}: {record_date_old_ship[i]}:{record_st_old_ship[i]}-{record_en_old_ship[i]}</span><br>"
        rec_user_new_ship = list(Records_ship.objects.filter(driver=user.pk).filter(date_start__gt=datetime.now()))
        record_date_ship = []
        record_st_ship = []
        record_en_ship = []
        records_pk_ship = []
        html_rec_user_new_ship = f""
        for i in range(0, len(rec_user_new_ship)):
            record_date_ship.append(rec_user_new_ship[i].date_start)
            record_st_ship.append(rec_user_new_ship[i].start_time)
            record_en_ship.append(rec_user_new_ship[i].end_time)
            records_pk_ship.append(rec_user_new_ship[i].pk)
        for i in range(0, len(records_pk_ship)):
            html_rec_user_new_ship += f"<span style='font-size: 18px;'>{prof_lastname} {prof_firstname}: {record_date_ship[i]}:{record_st_ship[i]}-{record_en_ship[i]}<a href='records/{records_pk_ship[i]}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a></span><br>"
        users = list(User.objects.all())
        user_first_name = []
        user_last_name = []
        user_username = []
        user_pk = []
        for i in range(0, len(users)):
            user_first_name.append(users[i].first_name)
            user_last_name.append(users[i].last_name)
            user_username.append(users[i].username)
            user_pk.append(users[i].pk)
        context = {'html_rec_user_old': html_rec_user_old,
                   'html_rec_user_old_ship': html_rec_user_old_ship,
                   'html_rec_user_new': html_rec_user_new,
                   'html_rec_user_new_ship': html_rec_user_new_ship,
                   'prof': prof,
                   'prof_email': prof_email,
                   'prof_firstname': prof_firstname,
                   'prof_lastname': prof_lastname,
                   'user_username': user_username,
                   'user_pk': user_pk}
        return render(request, 'records/admining_pk.html', context)


@login_required
def user_delete(request, username):
    if request.user.is_superuser:
        user = get_object_or_404(User, username=username)
        user.delete()
        return render(request, 'records/delete.html', context={'messages': 'Вы успешно удалили пользоваеля'})
    return render(request, 'records/records_admining_pk.html', context={'messages': 'У вас нету прав'})
