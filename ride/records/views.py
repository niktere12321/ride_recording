import calendar
from datetime import date, datetime, timedelta
from re import S

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic

from .decorathion import active, admin
from .forms import RecordsForm, ServicesForm
from .models import Records, Services
from .utils import (Calendar, get_week_card, line_day, send_email,
                    send_message, time_step)

User = get_user_model()


def index_services(request):
    """Выбор странички с транспортным средством"""
    if request.user.is_authenticated:
        if request.user.active == True:
            all_services = Services.objects.all()
            context = {
                'all_services': all_services,
            }
            return render(request, 'records/index_services.html', context)
        return redirect(reverse('users:help_active'))
    return redirect(reverse('users:login'))


class CalendarView(generic.ListView):
    """Основной календарь"""
    model = Records
    template_name = 'records/index_records.html'

    def get_context_data(self, **kwargs):
        """Основной календарь"""
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
    """Для основного календаря"""
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    """Для основного календаря"""
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    """Для основного календаря"""
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@active
@login_required
def records_start(request, date, project):
    """Создание записи для пользователя"""
    new_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
    date_str = date[6:] + '.' + date[4:6] +'.' + date[:4]
    d = get_date(date[:4] + '-' + date[4:6])
    month_now_for_url = f"month={date[:4]}-{date[4:6]}"
    month_now = date[4:6]
    date_record = datetime.strptime(new_date, '%Y-%m-%d').date()
    services = Services.objects.get(pk=project)
    time_now_to_rec = services.low_time
    if date_record == datetime.now().date():
        time_now_to_rec = datetime.now().time()
    record_list = list(Records.objects.filter(date_start=new_date, project=project))
    """получение полоски недели"""
    week_line = get_week_card(date_record, services, new_date, project)
    """Получение полоски показывающей загруженость дня"""
    get_int_low_time = time_step(services.low_time)
    get_int_high_time = time_step(services.high_time)
    record_list_for_line = Records.objects.filter(date_start=new_date, project=project).order_by('start_time')
    line = line_day(record_list_for_line, date_record, services)
    color_table = f"<div class='line_for_form'>{line}</div>"
    """Создание таблицы показывающей записи в этот день"""
    if len(record_list) > 0:
        ride_rec_empty = None
        user_list = list(User.objects.filter(active=True))
        ride_rec = f'''<th></th>
                       <th class="th_cal_record">Транспортное средство</th>
                       <th class="th_cal_record">Пользователя</th>
                       <th class="th_cal_record">Запись</th></tr>'''
        count_rec = 0
        for i in range(0, len(user_list)):
            records_to_user = list(Records.objects.filter(date_start=new_date, project=project, driver=user_list[i].pk).order_by('start_time'))
            for j in range(0, len(records_to_user)):
                count_rec += 1
                if request.user.role == 'admin' or request.user.pk == user_list[i].pk:
                    del_rec = f" <a href='../../../records/records/{records_to_user[j].pk}/delete/{project}/{date}/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a>"
                    ride_rec += f'<tr><td>{count_rec}</td><td>{services.name_project}</td><td>{user_list[i].first_name}</br>{user_list[i].last_name}</td><td>С {records_to_user[j].start_time} до {records_to_user[j].end_time} {del_rec}</td>'
                else:
                    ride_rec += f'<tr><td>{count_rec}</td><td>{services.name_project}</td><td>{user_list[i].first_name}</br>{user_list[i].last_name}</td><td>С {records_to_user[j].start_time} до {records_to_user[j].end_time}</td>'
            ride_rec += f'</tr>'
    else:
        ride_rec = None
        ride_rec_empty = f"<h1 style='text-align: center; margin-top: 10%;'>День полностью пуст</h1>"
    """Пповерка если выбранный день в прошлом"""
    if date_record < datetime.now().date():
        context = {"old_date": "Запись недоступна",
                   "ride_rec": ride_rec,
                   "ride_rec_empty": ride_rec_empty,
                   "color_table": color_table,
                   "new_date": new_date,
                   "date_str": date_str,
                   "prev_month": prev_month(d),
                   "next_month": next_month(d),
                   "month_now_for_url": month_now_for_url,
                   "month_now": month_now,
                   "get_int_low_time": get_int_low_time,
                   "get_int_high_time": get_int_high_time,
                   "date": date,
                   "project": project,
                   "week_line": week_line,
                   "record_list_for_line": record_list_for_line}
        return render(request, 'records/records_start.html', context)
    """Проверка усли у пользователя меньше 10 записей на это транспортное средство"""
    about_count = Records.objects.filter(driver=request.user.pk, project=project, date_start__gte=datetime.now()).count()
    if about_count >= 10:
        context = {'ride_rec': ride_rec,
                   'ride_rec_empty': ride_rec_empty,
                   'color_table': color_table,
                   'new_date': new_date,
                   "date_str": date_str,
                   'prev_month': prev_month(d),
                   'next_month': next_month(d),
                   "month_now_for_url": month_now_for_url,
                   "month_now": month_now,
                   'get_int_low_time': get_int_low_time,
                   'get_int_high_time': get_int_high_time,
                   'date': date,
                   'project': project,
                   'services': services,
                   'many_rec': 'Максимум записей 10',
                   'week_line': week_line,
                   "record_list_for_line": record_list_for_line}
        return render(request, 'records/records_start.html', context)
    """Создание формы"""
    form = RecordsForm(request.POST or None, project_to_validate=project, date_to_validate=new_date)
    if request.POST and form.is_valid() and (date_record >= datetime.now().date()):
        records = form.save(commit=False)
        records.date_start = new_date
        records.driver = request.user
        records.project = services
        start_ti = form.cleaned_data['start_time']
        end_ti = form.cleaned_data['end_time']
        records.start_time = start_ti
        records.end_time = end_ti
        records.save()
        """Отправка сообщения на почту пользователя и администратору на телеграмм"""
        send_email(request.user.email, services.name_project, request.user.first_name, request.user.last_name, new_date, start_ti, end_ti)
        send_message(f'{records.driver}:{new_date} с {start_ti} {end_ti}')
        return redirect(reverse('records:index_records', args=[project]))
    context = {'ride_rec': ride_rec,
               'ride_rec_empty': ride_rec_empty,
               'color_table': color_table,
               'form': form,
               'new_date': new_date,
               "date_str": date_str,
               'prev_month': prev_month(d),
               'next_month': next_month(d),
               "month_now_for_url": month_now_for_url,
               "month_now": month_now,
               'get_int_low_time': get_int_low_time,
               'get_int_high_time': get_int_high_time,
               'services': services,
               'time_now_to_rec': time_now_to_rec,
               'date': date,
               'project': project,
               'week_line': week_line,
               "record_list_for_line": list(record_list_for_line)}
    return render(request, 'records/records_start.html', context)


@active
@login_required
def profiles(request):
    """Профиль"""
    """Таблица записей пользователя в будующем"""
    user = User.objects.get(username=request.user.username)
    records_to_user_new = list(Records.objects.filter(date_start__gte=datetime.now().date(), driver=user).order_by('date_start','start_time'))
    if len(records_to_user_new) > 0:
        ride_rec = f'<tr><th></th><th>Транспортное средство</th><th>Дата</th><th>Запись</th></tr>'
        count_rec = 0
        for i in range(0, len(records_to_user_new)):
            services = get_object_or_404(Services, pk=int(records_to_user_new[i].project.pk))
            count_rec += 1
            del_rec = f" <a href='../../../records/records/{records_to_user_new[i].pk}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a>"
            ride_rec += f'<tr id="count_new"><td>{count_rec}</td><td>{services.name_project}</td><td>{records_to_user_new[i].date_start}</td><td>С {records_to_user_new[i].start_time} до {records_to_user_new[i].end_time} {del_rec}</td></tr>'
    else:
        ride_rec = f'<tr><th style="text-align: center">На сегоднишний день у вас нету записей в будующем</th></tr>'
    """Таблица записей пользователя в прошлом"""
    records_to_user_old = list(Records.objects.filter(date_start__lt=datetime.now().date(), driver=user).order_by('-date_start','-start_time'))
    if len(records_to_user_old) > 0:
        ride_rec_old = f'<tr><th></th><th>Транспортное средство</th><th>Дата</th><th>Запись</th></tr>'
        count_rec = 0
        for i in range(0, len(records_to_user_old)):
            services = get_object_or_404(Services, pk=int(records_to_user_old[i].project.pk))
            count_rec += 1
            ride_rec_old += f'<tr id="count_old"><td>{count_rec}</td><td>{services.name_project}</td><td>{records_to_user_old[i].date_start}</td><td>С {records_to_user_old[i].start_time} до {records_to_user_old[i].end_time}</td></tr>'
    else:
        ride_rec_old = f'<tr><th style="text-align: center">На сегоднишний день у вас нету записей в прошлом</th></tr>'
    context = {'ride_rec_old': ride_rec_old,
               'ride_rec': ride_rec,
               'prof': user}
    return render(request, 'records/profiles.html', context)


@active
@login_required
def records_delete(request, rec_pk, project, date):
    """Удаление записи"""
    records_del = get_object_or_404(Records, pk=rec_pk)
    if request.user == records_del.driver or request.user.role == 'admin':
        records_del.delete()
        context = {'messages': 'Вы успешно удалили запись'}
        return redirect(reverse('records:records_start', args=[project, date]))
    context = {'messages': 'У вас нету прав'}
    return render(request, 'records/index.html', context)


@admin
@active
@login_required
def admining(request):
    """Все транспортные средства"""
    all_services = Services.objects.all()
    context = {'all_services': all_services}
    return render(request, 'records/admining.html', context)


@admin
@active
@login_required
def admining_users(request):
    """Все пользователи"""
    all_users = User.objects.all()
    context = {'all_users': all_users}
    return render(request, 'records/admining_users.html', context)


@admin
@active
@login_required
def admining_services(request, service_id):
    """Информация транспортного средства"""
    services = get_object_or_404(Services, pk=service_id)
    context = {'services': services}
    return render(request, 'records/admining_services.html', context)


@admin
@active
@login_required
def admining_services_edit(request, services_id):
    """Измение данных транспортного средства"""
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


@admin
@active
@login_required
def admining_services_create(request):
    """Создание транспортного средства"""
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


@admin
@active
@login_required
def admining_services_del(request, services_id):
    """Удаление транспортоного средства"""
    if request.user.role == 'user':
        context = {'messages': 'У вас нету прав'}
        return render(request, 'records/index.html', context)
    services = get_object_or_404(Services, pk=services_id)
    services.delete()
    context = {'messages': 'Вы успешно удалили Транспортное средство'}
    return redirect(reverse('records:admining'))


@admin
@active
@login_required
def admining_statistics(request, pass_date, future_date):
    """Статистика проекта для администратора"""
    if pass_date == 'default' and future_date == 'default':
        pass_date = date.today().replace(day=1)
        if date.month == 12:
            future_date = date.replace(day=31)
        else:
            future_date = datetime.now().date().replace(month=datetime.now().month+1, day=1) - timedelta(days=1)
    """Общая статистика записей пользователей"""
    table_for_all_records = "<thead><tr><th>Пользователь</th>"
    all_services = list(Services.objects.all())
    for service in all_services:
        table_for_all_records += f"<th>Количество поездок на {service.name_project}</th>"
    table_for_all_records += "<th>Всего поездок</th></tr></thead><tbody>"
    all_user = list(User.objects.filter(active=True))
    counter_all_services_records = 0
    list_count = []
    for user in range(len(all_user)):
        table_for_all_records += f"<tr><td><a href='../../../records/admining/{all_user[user].username}'>{all_user[user].first_name} {all_user[user].last_name}</a></td>"
        counter_all_services = 0
        for service in range(len(all_services)):
            records_for_user = Records.objects.filter(driver=all_user[user], project=all_services[service].pk, date_start__gte=pass_date, date_start__lte=future_date)
            counter_records_to_service = 0
            for records in range(len(records_for_user)):
                counter_records_to_service += 1
                counter_all_services += 1
                counter_all_services_records += 1
            list_count.append(counter_records_to_service)
            table_for_all_records += f"<td>{counter_records_to_service}</td>"
        table_for_all_records += f"<td>{counter_all_services}</td></tr>"
    table_for_all_records += f"<tr><td>Итого</td>"
    for service in range(len(all_services)):
        all_records_for_service  = Records.objects.filter(project=all_services[service].pk, date_start__gte=pass_date, date_start__lte=future_date)
        count_rec = 0
        for records in range(len(all_records_for_service)):
            count_rec += 1
        table_for_all_records += f"<td>{count_rec}</td>"
    table_for_all_records += f"<td>{counter_all_services_records}</td></tr>"
    table_for_all_records += "</tbody>"
    # """Создание выпадающих списков"""
    # select_user = """<label for="select_user_input">Выбор пользователей:</label>
    # <input type='text' id='select_user_input' name='select_user' list='select_user'>
    # <datalist id='select_user'>"""
    # for i in all_user:
    #     select_user += f"<option class='label' value='{i.first_name} {i.last_name}'>"
    # select_user += "</datalist>"
    # select_services = """<label for="select_services_input">Выбор транспортого средства:</label>
    # <input type='text' id='select_services_input' name='select_services' list='select_services'>
    # <datalist id='select_services'>"""
    # for i in all_services:
    #     select_services += f"<option class='label' value='{i.name_project}'>"
    # select_services += "</datalist>"
    """Таблица будующих записей всех пользователей"""
    if str(pass_date) >= str(date.today()) and str(future_date) >= str(date.today()):
        records_to_user_new = list(Records.objects.filter(date_start__gte=pass_date, date_start__lte=future_date).order_by('date_start','start_time'))
    elif str(pass_date) <= str(date.today()) and str(future_date) >= str(date.today()):
        records_to_user_new = list(Records.objects.filter(date_start__gte=date.today(), date_start__lte=future_date).order_by('date_start','start_time'))
    else:
        records_to_user_new = []
    if len(records_to_user_new) > 0:
        ride_rec = f'<tr><th></th><th>Пользователь</th><th>Транспортное средство</th><th>Дата</th><th>Запись</th></tr>'
        count_rec = 0
        for i in range(0, len(records_to_user_new)):
            services = get_object_or_404(Services, pk=int(records_to_user_new[i].project.pk))
            count_rec += 1
            del_rec = f" <a href='../../../records/records/{records_to_user_new[i].pk}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a>"
            ride_rec += f'<tr id="count_new"><td>{count_rec}</td><td>{records_to_user_new[i].driver.first_name} {records_to_user_new[i].driver.last_name}</td><td>{services.name_project}</td><td>{records_to_user_new[i].date_start}</td><td>С {records_to_user_new[i].start_time} до {records_to_user_new[i].end_time} {del_rec}</td></tr>'
    else:
        ride_rec = f'<tr><th style="text-align: center">С {pass_date} до {future_date} нету новых записей</th></tr>'
    """Таблица прошлых записей всех пользователей"""
    if str(pass_date) <= str(date.today()) and str(future_date) <= str(date.today()):
        records_to_user_old = list(Records.objects.filter(date_start__gte=pass_date, date_start__lte=future_date).order_by('-date_start','-start_time'))
    elif str(pass_date) <= str(date.today()) and str(future_date) >= str(date.today()):
        records_to_user_old = list(Records.objects.filter(date_start__gte=pass_date, date_start__lte=date.today()).order_by('-date_start','-start_time'))
    else:
        records_to_user_old = []
    if len(records_to_user_old) > 0:
        ride_rec_old = f'<tr><th></th><th>Пользователь</th><th>Транспортное средство</th><th>Дата</th><th>Запись</th></tr>'
        count_rec = 0
        for i in range(0, len(records_to_user_old)):
            services = get_object_or_404(Services, pk=int(records_to_user_old[i].project.pk))
            count_rec += 1
            ride_rec_old += f'<tr id="count_old"><td>{count_rec}</td><td>{records_to_user_old[i].driver.first_name} {records_to_user_old[i].driver.last_name}</td><td>{services.name_project}</td><td>{records_to_user_old[i].date_start}</td><td>С {records_to_user_old[i].start_time} до {records_to_user_old[i].end_time}</td></tr>'
    else:
        ride_rec_old = f'<tr><th style="text-align: center">С {pass_date} до {future_date} нету прошедших записей</th></tr>'
    """Диаграмма самых активных пользователей"""
    all_active_records = {}
    list_active_records = []
    all_procent_records = 0
    for user in range(len(all_user)):
        count_records = 0
        all_records_for_user = Records.objects.filter(driver=all_user[user], date_start__gte=pass_date, date_start__lte=future_date)
        for record in range(len(all_records_for_user)):
            count_records += 1
            all_procent_records += 1
        all_active_records[count_records] = all_user[user]
        list_active_records.append(count_records)
    list_active_records.sort(reverse=True)
    list_active_records_to_read = ''
    first_piechart = 0
    second_piechart = 0
    third_piechart = 0
    no_other_records = 0
    for i in range(len(list_active_records)):
        if i == 0:
            user = get_object_or_404(User, username=str(all_active_records[list_active_records[i]]))
            text_user = user.first_name + ' ' + user.last_name
            text_user_records = str(list_active_records[i]) + ' записей'
            list_active_records_to_read += f"<p>{text_user_records}: {text_user}</p>"
            if all_procent_records != 0:
                first_piechart = list_active_records[i] / all_procent_records * 360
            else:
                first_piechart = 0
            no_other_records += list_active_records[i]
            other_piechart = 360 - first_piechart
        elif i == 1:
            user = get_object_or_404(User, username=str(all_active_records[list_active_records[i]]))
            text_user = user.first_name + ' ' + user.last_name
            text_user_records = str(list_active_records[i]) + ' записей'
            list_active_records_to_read += f"<p>{text_user_records}: {text_user}</p>"
            if all_procent_records != 0:
                second_piechart = first_piechart + list_active_records[i] /all_procent_records * 360
            else:
                second_piechart = 0
            no_other_records += list_active_records[i]
            other_piechart = 360 - second_piechart
        elif i == 2:
            user = get_object_or_404(User, username=str(all_active_records[list_active_records[i]]))
            text_user = user.first_name + ' ' + user.last_name
            text_user_records = str(list_active_records[i]) + ' записей'
            list_active_records_to_read += f"<p>{text_user_records}: {text_user}</p>"
            if all_procent_records != 0:
                third_piechart = second_piechart + list_active_records[i] /all_procent_records * 360
            else:
                third_piechart = 0
            no_other_records += list_active_records[i]
            other_piechart = 360 - third_piechart
        else:
            no_other_records += list_active_records[i]
    other_records = str(all_procent_records - no_other_records) + ' записей'
    piechart_for_all_records = f"background-image: conic-gradient(pink {first_piechart}deg, lightblue 0 {second_piechart}deg, orange 0 {third_piechart}deg, gray 0 {other_piechart}deg);"
    list_active_records_to_read += f"<p>Остальные: {other_records}</p>"
    """Диаграмма популярности транспортых средств"""
    list_services = []
    list_dict = {}
    count_all_services = 0
    for service in all_services:
        count_services = 0
        all_records_for_service = Records.objects.filter(project=service.pk, date_start__gte=pass_date, date_start__lte=future_date)
        for record in all_records_for_service:
            count_services += 1
            count_all_services += 1
        list_services.append(count_services)
        list_dict[count_services] = service.name_project
    list_services.sort(reverse=True)
    list_services_text = ''
    for i in range(len(list_services)):
        if i == 0:
            first_services = get_object_or_404(Services, name_project=str(list_dict[list_services[i]])).name_project
            first_services_records = str(list_services[i]) + ' записей'
            list_services_text += f"<p>{first_services}: {first_services_records}</p>"
            if all_procent_records != 0:
                first_piechart = list_services[i] /all_procent_records * 360
            else:
                first_piechart = 0
            other_piechart = 360 - second_piechart
        elif i == 1:
            second_services = get_object_or_404(Services, name_project=str(list_dict[list_services[i]])).name_project
            second_services_records = str(list_services[i]) + ' записей'
            list_services_text += f"<p>{second_services}: {second_services_records}</p>"
            if all_procent_records != 0:
                second_piechart = first_piechart + list_services[i] /all_procent_records * 360
            else:
                second_piechart = 0
            other_piechart = 360 - second_piechart
    piechart_for_services = f"background-image: conic-gradient(blue {first_piechart}deg, red 0 {second_piechart}deg, gray 0 {other_piechart}deg);"
    """Даты для выбора ссылок"""
    all_year_pass = datetime.now().date().replace(day=1, month=1)
    all_year_future = datetime.now().date().replace(day=31, month=12)
    on_month_pass = datetime.now().date()
    on_month_future = datetime.now().date().replace(month=datetime.now().month+2, day=1) - timedelta(days=1)
    on_month_pass_old = (datetime.now().date() - timedelta(days=31))
    on_month_future_old = datetime.now().date().replace(month=datetime.now().month+2, day=1) - timedelta(days=1)
    on_half_year_pass = (datetime.now().date() - timedelta(days=183))
    on_half_year_future = datetime.now().date()
    on_half_year_pass_new = datetime.now().date
    on_half_year_future_new = (datetime.now().date() + timedelta(days=183))
    context = {'pass_date': pass_date,
               'future_date': future_date,
               'table_for_all_records': table_for_all_records,
            #    'select_user': select_user,
            #    'select_services': select_services,
               'ride_rec': ride_rec,
               'ride_rec_old': ride_rec_old,
               'piechart_for_all_records': piechart_for_all_records,
               'list_active_records_to_read': list_active_records_to_read,
               'piechart_for_services': piechart_for_services,
               'list_services': list_services_text,
               'all_year_pass': all_year_pass,
               'all_year_future': all_year_future,
               'on_month_pass': on_month_pass,
               'on_month_future': on_month_future,
               'on_month_pass_old': on_month_pass_old,
               'on_month_future_old': on_month_future_old,
               'on_half_year_pass': on_half_year_pass,
               'on_half_year_future': on_half_year_future,
               'on_half_year_pass_new': on_half_year_pass_new,
               'on_half_year_future_new': on_half_year_future_new}
    return render(request, 'records/admining_statistics.html', context)


@admin
@active
@login_required
def admining_pk(request, username):
    """"Аккаунты пользователей для администратора"""
    """Таблица всех записей пользователя в будующем"""
    user = get_object_or_404(User, username=username)
    records_to_user_new = list(Records.objects.filter(date_start__gte=datetime.now().date(), driver=user).order_by('date_start','start_time'))
    if len(records_to_user_new) > 0:
        ride_rec = f'<tr><th></th><th>Транспортное средство</th><th>Дата</th><th>Запись</th></tr>'
        count_rec = 0
        for i in range(0, len(records_to_user_new)):
            services = get_object_or_404(Services, pk=int(records_to_user_new[i].project.pk))
            count_rec += 1
            del_rec = f" <a href='../../../records/records/{records_to_user_new[i].pk}/delete/' onclick=\"return confirm('Вы уверены что хотите удалить?')\"> удалить ?</a>"
            ride_rec += f'<tr id="count_new"><td>{count_rec}</td><td>{services.name_project}</td><td>{records_to_user_new[i].date_start}</td><td>С {records_to_user_new[i].start_time} до {records_to_user_new[i].end_time} {del_rec}</td></tr>'
    else:
        ride_rec = f'<tr><th style="text-align: center">На сегоднишний день у пользователя нету записей в будующем</th></tr>'
    """Таблица всех записей пользователя в прошлом"""
    records_to_user_old = list(Records.objects.filter(date_start__lt=datetime.now().date(), driver=user).order_by('-date_start','-start_time'))
    if len(records_to_user_old) > 0:
        ride_rec_old = f'<tr><th></th><th>Транспортное средство</th><th>Дата</th><th>Запись</th></tr>'
        count_rec = 0
        for i in range(0, len(records_to_user_old)):
            services = get_object_or_404(Services, pk=int(records_to_user_old[i].project.pk))
            count_rec += 1
            ride_rec_old += f'<tr id="count_old"><td>{count_rec}</td><td>{services.name_project}</td><td>{records_to_user_old[i].date_start}</td><td>С {records_to_user_old[i].start_time} до {records_to_user_old[i].end_time}</td></tr>'
    else:
        ride_rec_old = f'<tr><th style="text-align: center">На сегоднишний день у пользователя нету записей в прошлом</th></tr>'
    active = ""
    """Кружочек определения статуса аккаунта пользователей"""
    if user.active == True:
        status = True
        active = "<div id='active'></div>"
    else:
        status = None
        active = "<div id='pass' style='display: table-sell;'></div>"
    context = {'ride_rec_old': ride_rec_old,
               'ride_rec': ride_rec,
               'prof': user,
               'status': status,
               'active': active}
    return render(request, 'records/admining_pk.html', context)


@admin
@active
@login_required
def user_delete(request, username):
    """Удаление пользователя"""
    if request.user.role == 'user':
        context = {'messages': 'У вас нету прав'}
        return render(request, 'records/records_admining_pk.html', context)
    user = get_object_or_404(User, username=username)
    user.delete()
    context = {'messages': 'Вы успешно удалили пользоваеля'}
    return redirect(reverse('records:admining_users'))


@admin
@active
@login_required
def user_pass_or_active(request, username):
    """Изменение статуса аккаунта пользователя"""
    if request.user.role == 'user':
        context = {'messages': 'У вас нету прав'}
        return render(request, 'records/records_admining_pk.html', context)
    user = get_object_or_404(User, username=username)
    if user.active == True:
        user.active = False
        user.save()
        context = {'messages': 'Вы успешно заблокировали пользоваеля', 'pass': 'pass'}
        return render(request, 'records/delete.html', context)
    elif user.active == False:
        user.active = True
        user.save()
        context = {'messages': 'Вы успешно разблокировали пользоваеля', 'active': 'active'}
        return render(request, 'records/delete.html', context)
