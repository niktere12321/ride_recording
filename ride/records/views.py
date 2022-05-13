import calendar
from datetime import date, datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic

from .forms import RecordsForm, ServicesForm
from .models import Records, Services
from .utils import Calendar, send_email, send_message

User = get_user_model()


@login_required
def index_services(request):
    all_services = Services.objects.all()
    context = {
        'all_services': all_services,
    }
    return render(request, 'records/index_services.html', context)


class CalendarView(generic.ListView):
    model = Records
    template_name = 'records/index_records.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        project = self.kwargs['project']
        cal = Calendar(d.year, d.month, project)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['project'] = project
        context['project_name'] = Services.objects.get(pk=project).name_project
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
def records_start(request, date, project):
    new_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
    new_date_str = date[6:] + '.' + date[4:6] + '.' + date[:4]
    services = Services.objects.get(pk=project)
    record_list = list(Records.objects.filter(date_start=new_date, project=project))
    record_list_p = list(Records.objects.filter(date_start=new_date))
    lol_red = f"<div style='height: 30px; width: 50px; background: red; display: table-cell;'> </div>"
    lol_green = f"<div style='height: 30px; width: 50px; background: green; display: table-cell;'> </div>"
    col = []
    for i in range(services.low_time, services.high_time):
        col.append(lol_green)
    for p in record_list:
        counter = 0
        for i in range(services.low_time, services.high_time):
            time_i = datetime.strptime(f"{i}:00:00", "%H:%M:%S")
            time_start = datetime.strptime(str(p.start_time), "%H:%M:%S")
            time_end = datetime.strptime(str(p.end_time), "%H:%M:%S")
            if time_i >= time_start and time_i < time_end:
                col[counter] = lol_red
            counter += 1
    line_1 = f""
    for i in range(len(col)):
        line_1 += col[i]
    color_table = f"<div style='max-width: 100%; height: 30px; margin: 5px 5px 0px 5px;'>{line_1}</div>"
    ride_rec = ''
    for i in range(0, len(record_list)):
        del_rec = f" <a href='../../../records/records/{record_list[i].pk}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a>"
        if (i % 3) == 0 and i != 0:
            if request.user.is_superuser:
                ride_rec += f"<span>{record_list[i].driver}: Время с {record_list[i].start_time} до {record_list[i].end_time} {del_rec}</span><br>"
            else:
                ride_rec += f"<span>{record_list[i].driver}:Время с {record_list[i].start_time} до {record_list[i].end_time}</span><br>"
        else:
            if request.user.is_superuser:
                ride_rec += f"<span>{record_list[i].driver}: Время с {record_list[i].start_time} до {record_list[i].end_time} {del_rec}</span>"
            else:
                ride_rec += f"<span>{record_list[i].driver}: Время с {record_list[i].start_time} до {record_list[i].end_time};  </span>"
    ride_rec_empty = None
    if ride_rec == "":
        ride_rec_empty = "День полностью пустой"
    month_ride = int(date[4:6])
    d = get_date(request.GET.get('month', None))
    cal = Calendar(d.year, month_ride, project)
    html_cal = cal.formatmonth(withyear=True)
    if datetime.strptime(new_date, '%Y-%m-%d') <= datetime.now():
        context = {'ride_rec': ride_rec,
                   'color_table': color_table,
                   'calendar': mark_safe(html_cal),
                   'date_str': new_date_str,
                   'date': date,
                   'project': project,
                   'services': services,
                   'ride_rec_empty': ride_rec_empty,
                   'old_date': "Доступна только история дней минувших"}
        return render(request, 'records/records_start.html', context)
    pk_user = User.objects.get(username=request.user.username).id
    about_count = Records.objects.filter(driver=pk_user, project=project, date_start__gt=datetime.now()).count()
    if about_count == 10:
        context = {'ride_rec': ride_rec,
                   'color_table': color_table,
                   'calendar': mark_safe(html_cal),
                   'date_str': new_date_str,
                   'date': date,
                   'project': project,
                   'services': services,
                   'ride_rec_empty': ride_rec_empty,
                   'many_rec': "Максимум записей 10"}
        return render(request, 'records/records_start.html', context)
    form = RecordsForm(request.POST or None)
    if request.POST and form.is_valid() and (datetime.strptime(new_date, '%Y-%m-%d') > datetime.now()):
        records = form.save(commit=False)
        records.date_start = new_date
        records.driver = request.user
        records.project = services
        start_ti = form.cleaned_data['start_time']
        end_ti = form.cleaned_data['end_time']
        if start_ti > end_ti:
            context = {"error": f"Введите корректное время поездки.",
                       "date": date,
                       "project": project}
            return render(request, 'records/records_start.html', context)
        if datetime.strptime((end_ti.timestamp() - start_ti.timestamp()), "%H:%M:%S") > datetime.strptime(f'{services.high_duration}:00:00', "%H:%M:%S"):
            context = {"error": f"Нельзя кататься больше {services.high_duration} часов",
                       "date": date,
                       "project": project}
            return render(request, 'records/records_start.html', context)
        if (end_ti - start_ti) <= services.low_duration:
            context = {"error": f"Нельзя кататься меньше {services.low_duration} часов",
                       "date": date,
                       "project": project}
            return render(request, 'records/records_start.html', context)
        record_st_p = []
        record_en_p = []
        for i in range(0, len(record_list_p)):
            record_st_p.append(record_list_p[i].start_time)
            record_en_p.append(record_list_p[i].end_time)
        for i in record_st_p:
            for p in record_en_p:
                if (start_ti >= i and end_ti <= p) or (start_ti > i and start_ti < p and end_ti > p):
                    context = {"error": f"В это время вы уже катаетесь на другом т.с.",
                               "date": date,
                               "project": project}
                    return render(request, 'records/records_start.html', context)
                elif start_ti < i and end_ti <= i:
                    break
                elif start_ti < i and end_ti < p:
                    context = {"error": f"В это время вы уже катаетесь на другом т.с.",
                               "date": date,
                               "project": project}
                    return render(request, 'records/records_start.html', context)
        record_st = []
        record_en = []
        for i in range(0, len(record_list)):
            record_st.append(record_list[i].start_time)
            record_en.append(record_list[i].end_time)
        for i in record_st:
            for p in record_en:
                if (start_ti >= i and end_ti <= p) or (start_ti > i and start_ti < p and end_ti > p):
                    context = {"error": "Это время уже занято!",
                               "date": date,
                               "project": project}
                    return render(request, 'records/records_start.html', context)
                elif start_ti < i and end_ti <= i:
                    break
                elif start_ti < i and end_ti <= p:
                    context = {"error": "Это время уже занято!",
                               "date": date,
                               "project": project}
                    return render(request, 'records/records_start.html', context)
        records.start_time = start_ti
        records.end_time = end_ti
        records.save()
        send_email(request.user.email, services.name_project, request.user.first_name, request.user.last_name, new_date, start_ti, end_ti)
        send_message(f'{records.driver}:{new_date} с {start_ti} {end_ti}')
        return redirect(reverse('records:index_records', args=[project]))
    context = {'ride_rec': ride_rec,
               'color_table': color_table,
               'form': form,
               'calendar': mark_safe(html_cal),
               'date_str': new_date_str,
               'services': services,
               'ride_rec_empty': ride_rec_empty,
               'date': date}
    return render(request, 'records/records_start.html', context)


@login_required
def profiles(request):
    user = User.objects.get(username=request.user.username)
    all_services = list(Services.objects.filter(pk__gt=0))
    html_rec_new = f""
    for p in range(len(all_services)):
        rec_new = list(Records.objects.filter(driver=user.pk, project=all_services[p].pk, date_start__gt=datetime.now()))
        html_rec_new += f"<h4>{all_services[p].name_project}<h4>"
        for i in range(0, len(rec_new)):
            del_rec = f"<a href='records/{rec_new[i].pk}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a>"
            html_rec_new += f"<span style='font-size: 18px;'>{user.last_name} {user.first_name}: {rec_new[i].date_start}:{rec_new[i].start_time}-{rec_new[i].end_time}{del_rec}</span><br>"
    html_rec_old = f""
    for p in range(len(all_services)):
        rec_old = list(Records.objects.filter(driver=user.pk, project=all_services[p].pk, date_start__lte=datetime.now()))
        html_rec_old += f"<h4>{all_services[p].name_project}<h4>"
        for i in range(0, len(rec_old)):
            html_rec_old += f"<span style='font-size: 18px;'>{user.last_name} {user.first_name}: {rec_old[i].date_start}:{rec_old[i].start_time}-{rec_old[i].end_time}</span><br>"
    context = {'html_rec_old': html_rec_old,
               'html_rec_new': html_rec_new,
               'prof': user}
    return render(request, 'records/profiles.html', context)


@login_required
def records_delete(request, rec_pk):
    records_del = get_object_or_404(Records, pk=rec_pk)
    if request.user == records_del.driver or request.user.is_superuser:
        records_del.delete()
        context = {'messages': 'Вы успешно удалили запись'}
        return render(request, 'records/delete.html', context)
    context = {'messages': 'У вас нету прав'}
    return render(request, 'records/index.html', context)


@login_required
def admining(request):
    if request.user.is_superuser:
        all_services = Services.objects.all()
        context = {'all_services': all_services}
        return render(request, 'records/admining.html', context)


@login_required
def admining_users(request):
    if request.user.is_superuser:
        all_users = User.objects.all()
        context = {'all_users': all_users}
        return render(request, 'records/admining_users.html', context)


@login_required
def admining_services(request, service_id):
    if request.user.is_superuser:
        services = Services.objects.get(pk=service_id)
        context = {'services': services}
        return render(request, 'records/admining_services.html', context)


@login_required
def admining_services_edit(request, services_id):
    if request.user.is_superuser:
        services = get_object_or_404(Services, pk=services_id)
        form = ServicesForm(
            request.POST or None,
            files=request.FILES or None,
            instance=services
        )
        if request.POST and form.is_valid():
            form.save()
        else:
            context = {'form': form,
                       'services': services}
            return render(request, 'records/create_services.html', context)
        return redirect(reverse('records:admining_services', args=[services_id]))


@login_required
def admining_services_create(request):
    if request.user.is_superuser:
        form = ServicesForm(request.POST or None)
        if request.POST and form.is_valid():
            name_project = form.cleaned_data['name_project']
            name_exists = name_project is not None and Services.objects.filter(name_project=name_project).exists()
            if name_exists:
                context = {'form': form,
                           'error': 'Это транспортное средство уже существует.'}
                return render(request, 'records/create_services.html', context)
            form.name_project = name_project
            form.save()
        else:
            context =  {'form': form}
            return render(request, 'records/create_services.html', context)
        return redirect(reverse('records:admining'))


@login_required
def admining_services_del(request, services_id):
    if request.user.is_superuser:
        services = get_object_or_404(Services, pk=services_id)
        services.delete()
        context = {'messages': 'Вы успешно удалили Транспортное средство'}
        return render(request, 'records/delete.html', context)
    context = {'messages': 'У вас нету прав'}
    return render(request, 'records/index.html', context)


@login_required
def admining_statistics(request):
    if request.user.is_superuser:
        context = {'1': 1}
        return render(request, 'records/admining_statistics.html', context)


@login_required
def admining_pk(request, username):
    if request.user.is_superuser:
        user = get_object_or_404(User, username=username)
        all_services = list(Services.objects.filter(pk__gt=0))
        html_rec_new = f""
        for p in range(len(all_services)):
            rec_new = list(Records.objects.filter(driver=user.pk, project=all_services[p].pk, date_start__gt=datetime.now()))
            html_rec_new += f"<h4>{all_services[p].name_project}<h4>"
            for i in range(0, len(rec_new)):
                del_rec = f"<a href='../records/{rec_new[i].pk}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a>"
                html_rec_new += f"<span style='font-size: 18px;'>{user.last_name} {user.first_name}: {rec_new[i].date_start}:{rec_new[i].start_time}-{rec_new[i].end_time}{del_rec}</span><br>"
        html_rec_old = f""
        for p in range(len(all_services)):
            rec_old = list(Records.objects.filter(driver=user.pk, project=all_services[p].pk, date_start__lte=datetime.now()))
            html_rec_old += f"<h4>{all_services[p].name_project}<h4>"
            for i in range(0, len(rec_old)):
                html_rec_old += f"<span style='font-size: 18px;'>{user.last_name} {user.first_name}:{rec_old[i].date_start}:{rec_old[i].start_time}-{rec_old[i].end_time}</span><br>"
        context = {'html_rec_old': html_rec_old,
                   'html_rec_new': html_rec_new,
                   'prof': user}
        return render(request, 'records/admining_pk.html', context)


@login_required
def user_delete(request, username):
    if request.user.is_superuser:
        user = get_object_or_404(User, username=username)
        user.delete()
        context = {'messages': 'Вы успешно удалили пользоваеля'}
        return render(request, 'records/delete.html', context)
    context = {'messages': 'У вас нету прав'}
    return render(request, 'records/records_admining_pk.html', context)
