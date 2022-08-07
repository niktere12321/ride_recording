import datetime
import locale
import logging
from calendar import HTMLCalendar

import telegram
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

from .models import Records, Services

TELEGRAM_TOKEN = '2033287598:AAFBPr75b4abzYk0rMSH2Q4ph9mvMmC1U38'
CHAT_ID = '1495697329'

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def send_message(message):
    """Отправка сообщение администратору в телеграмм"""
    text = message
    try:
        bot.send_message(CHAT_ID, text)
    except Exception as e:
        logging.error(e, exc_info=True)
        return HttpResponse('Произошла ошибка повторите позже.')


def send_email(to_email, name_project, first_name, last_name, date, start_time, end_time):
    """Отравка сообщения на почту"""
    email = [to_email]
    email_from = settings.EMAIL_HOST_USER
    subject = f'Вы записались на {name_project}'
    message = f'{first_name} {last_name} вы записались на {name_project} {date} с {start_time} по {end_time}'
    try:
        send_mail(subject, message, email_from, email)
    except Exception as e:
        return HttpResponse('Произошла ошибка.')


def convert_time(time):
    time_str = str(time).split(':')
    time_all = int(time_str[0])*3600 + int(time_str[1])*60 + int(time_str[2])
    return time_all


def get_time(num, time_min):
    hours = (num + time_min) // 12 
    minuts = (num + time_min) % 12 * 5
    if minuts == '0':
        minuts = '00'
    if minuts == '5':
        minuts = '05'
    return f"{hours}:{minuts}:00"


def time_step(time):
    time_hours = int(str(time)[0:2])
    time_minuts = int(str(time)[3:5])
    int_time = time_hours * 12 + time_minuts // 5
    return int_time


def line_day(events_per_day, date_day, services, day=1):
    """Получение полоски показывающей загруженость дня"""
    list_color = []
    list_number = []
    young_time = time_step(services.low_time)
    old_time = time_step(services.high_time)
    if day != 0:
        if date_day < datetime.datetime.now().date():
            if len(events_per_day) > 0:
                for index, record in enumerate(events_per_day):
                    time_start = time_step(record.start_time)
                    time_end = time_step(record.end_time)
                    if index == 0:
                        list_color.append('brown')
                        list_number.append(time_start - young_time)
                        list_color.append('red')
                        list_number.append(time_end - time_start)
                        if index+1 == len(events_per_day):
                            list_color.append('brown')
                            list_number.append(old_time - time_end)
                        else:
                            pass
                    else:
                        list_color.append('brown')
                        list_number.append(time_start - time_step(events_per_day[index-1].end_time))
                        list_color.append('red')
                        list_number.append(time_end - time_start)
                        if index+1 == len(events_per_day):
                            list_color.append('brown')
                            list_number.append(old_time - time_end)
                        else:
                            pass
            else:
                list_color.append('brown')
                list_number.append(old_time - young_time)
        elif date_day == datetime.datetime.now().date():
            time_now = time_step(datetime.datetime.now().time())
            if len(events_per_day) > 0:
                for index, record in enumerate(events_per_day):
                    time_start = time_step(record.start_time)
                    time_end = time_step(record.end_time)
                    if index == 0:
                        if time_start <= time_now:
                            list_color.append('green')
                            list_number.append(time_start - young_time)
                            list_color.append('red')
                            list_number.append(time_end - time_start)
                            if index+1 == len(events_per_day):
                                if time_end < time_now:
                                    list_color.append('brown')
                                    list_number.append(time_now - time_end)
                                    list_color.append('green')
                                    list_number.append(old_time - time_now)
                                else:
                                    list_color.append('green')
                                    list_number.append(old_time - time_end)
                            else:
                                pass
                        elif time_start > time_now:
                            list_color.append('brown')
                            list_number.append(time_now - young_time)
                            list_color.append('green')
                            list_number.append(time_start - time_now)
                            list_color.append('red')
                            list_number.append(time_end - time_start)
                            if index+1 == len(events_per_day):
                                list_color.append('green')
                                list_number.append(old_time - time_end)
                            else:
                                pass
                    else:
                        if time_start <= time_now:
                            list_color.append('green')
                            list_number.append(time_start - time_step(events_per_day[index-1].end_time))
                            list_color.append('red')
                            list_number.append(time_end - time_start)
                            if index+1 == len(events_per_day):
                                if time_end < time_now:
                                    list_color.append('brown')
                                    list_number.append(time_now - time_end)
                                    list_color.append('green')
                                    list_number.append(old_time - time_now)
                                else:
                                    list_color.append('green')
                                    list_number.append(old_time - time_end)
                            else:
                                pass
                        elif time_start > time_now:
                            list_color.append('green')
                            list_number.append(time_start - time_step(events_per_day[index-1].end_time))
                            list_color.append('red')
                            list_number.append(time_end - time_start)
                            if index+1 == len(events_per_day):
                                list_color.append('green')
                                list_number.append(old_time - time_end)
                            else:
                                pass
            else:
                list_color.append('brown')
                list_number.append(time_now - young_time)
                list_color.append('green')
                list_number.append(old_time - time_now)
        else:
            if len(events_per_day) > 0:
                for index, record in enumerate(events_per_day):
                    time_start = time_step(record.start_time)
                    time_end = time_step(record.end_time)
                    if index == 0:
                        list_color.append('green')
                        list_number.append(time_start - young_time)
                        list_color.append('red')
                        list_number.append(time_end - time_start)
                        if index+1 == len(events_per_day):
                            list_color.append('green')
                            list_number.append(old_time - time_end)
                        else:
                            pass
                    else:
                        list_color.append('green')
                        list_number.append(time_start - time_step(events_per_day[index-1].end_time))
                        list_color.append('red')
                        list_number.append(time_end - time_start)
                        if index+1 == len(events_per_day):
                            list_color.append('green')
                            list_number.append(old_time - time_end)
                        else:
                            pass
            else:
                list_color.append('green')
                list_number.append(old_time - young_time)
    line = ""
    for i, color in enumerate(list_color):
        if color == 'brown':
            line += f'<div style="display: flex; border-radius: 10px; height: 40px; width: {list_number[i] / (old_time - young_time) * 100}%; background: #808080;"> </div>'
        elif color == 'red':
            line += f'<div style="display: flex; border-radius: 10px; height: 40px; width: {list_number[i] / (old_time - young_time) * 100}%; background: #FD6060;"> </div>'
        else:
            line += f'<div style="display: flex; border-radius: 10px; height: 40px; width: {list_number[i] / (old_time - young_time) * 100}%; background: #08B408;"> </div>'
    return line


class Calendar(HTMLCalendar):
    """Создание основного календаря"""
    def __init__(self, year=None, month=None, project=None):
        self.year = year
        self.month = month
        self.project = project
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(date_start__day=day).order_by('start_time')
        services = Services.objects.get(pk=self.project)
        if day != 0:
            date_day = datetime.datetime.strptime(f"{self.year}-{self.month}-{day}", "%Y-%m-%d").date()
            line = line_day(events_per_day, date_day, services, day)
        """Создание Id для дня с изменением цвета"""
        day_color = ''
        date_now = datetime.datetime.strptime(str(datetime.datetime.now().date()), "%Y-%m-%d").date()
        if day != 0:
            if date_day == date_now:
                day_color = "now_day_color"
                day_yes_or_no = f'<p class="record_yes_or_not">Запись доступна с {str(datetime.datetime.now().time())[0:5]} до {str(services.high_time)[0:5]}</p>'
            elif date_day <= date_now:
                day_color = "pass_day_color"
                day_yes_or_no = f'<p class="record_yes_or_not">Запись недоступна</p>'
            else:
                day_color = "future_day_color"
                day_yes_or_no = f'<p class="record_yes_or_not">Запись доступна с {str(services.low_time)[0:5]} до {str(services.high_time)[0:5]}</p>'
        """Перечень месяцев в склонении"""
        month_name = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
        """Создание ячейки дня с ссылкой"""
        if day != 0 and day < 10 and self.month < 10:
            return f"""<td class={day_color}>
                    <div class='div_in_table_days'>
                    <a href='{self.project}/records/{ self.year }0{ self.month }0{ day }/'>
                    <span class='day_in_week'>{day} {month_name[self.month]}</span>
                    {day_yes_or_no }
                    <div class='line_in_table'>{line}</div>
                    </a>
                    </div></td>"""
        elif day != 0 and day >= 10 and self.month < 10:
            return f"""<td class={day_color}>
                    <div class='div_in_table_days'>
                    <a href='{self.project}/records/{ self.year }0{ self.month }{ day }/'>
                    <span class='day_in_week'>{day} {month_name[self.month]}</span>
                    {day_yes_or_no }
                    <div class='line_in_table'>{line}</div>
                    </a>
                    </div></td>"""
        elif day != 0 and day < 10 and self.month >= 10:
            return f"""<td class={day_color}>
                    <div class='div_in_table_days'>
                    <a href='{self.project}/records/{ self.year }{ self.month }0{ day }/'>
                    <span class='day_in_week'>{day} {month_name[self.month]}</span>
                    {day_yes_or_no }
                    <div class='line_in_table'>{line}</div>
                    </a>
                    </div></td>"""
        elif day != 0 and day >= 10 and self.month >= 10:
            return f"""<td class={day_color}>
                    <div class='div_in_table_days'>
                    <a href='{self.project}/records/{ self.year }{ self.month }{ day }/'>
                    <span class='day_in_week'>{day} {month_name[self.month]}</span>
                    {day_yes_or_no }
                    <div class='line_in_table'>{line}</div>
                    </a>
                    </div></td>"""
        return f"<td></td>"

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        events = Records.objects.filter(date_start__year=self.year, date_start__month=self.month, project=self.project)
        week_day = f'''<tr><th class="text_day_in_week" id="border-left"> Пн </th>'
                    <th class="text_day_in_week"> Вт </th><th class="text_day_in_week">
                    Ср </th><th class="text_day_in_week"> Чт </th><th class="text_day_in_week">
                    Пт </th><th class="text_day_in_week"> Сб </th><th class="text_day_in_week" id="border-right"> Вс </th></tr>'''
        cal = f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{week_day}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal


def get_week_card(date_record, services, new_date, project):
    month_name = ['', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    date_now = datetime.datetime.strptime(str(datetime.datetime.now().date()), "%Y-%m-%d").date()
    date_for_week = datetime.datetime.strptime(new_date, '%Y-%m-%d')
    number_week = datetime.datetime.date(date_for_week).isocalendar()[1]
    record_list_for_week = Records.objects.filter(project=project)
    week_line = []
    for day_in_week in range(7):
        week_date = datetime.datetime.strptime(f"{str(new_date[:4])}" + "-W{}".format(number_week) + '-{}'.format(day_in_week), "%Y-W%W-%w").date()
        date_in_day = record_list_for_week.filter(date_start=week_date).order_by('start_time')
        if week_date == date_now:
            day_color = "now_day_color"
            day_yes_or_no = f'<p class="record_yes_or_not">Запись доступна с {str(datetime.datetime.now().time())[0:5]} до {str(services.high_time)[0:5]}</p>'
        elif week_date <= date_now:
            day_color = "pass_day_color"
            day_yes_or_no = f'<p class="record_yes_or_not">Запись недоступна</p>'
        else:
            day_color = "future_day_color"
            day_yes_or_no = f'<p class="record_yes_or_not">Запись доступна с {str(services.low_time)[0:5]} до {str(services.high_time)[0:5]}</p>'
        line = line_day(date_in_day, week_date, services)
        week_line.append(f"""<a href="../../../{project}/records/{str(week_date).replace('-', '')}/"><div class="day_in_record_week {day_color}"><span class="day_in_week">{str(week_date)[8:11]} {month_name[int(str(week_date).split('-')[1])]}</span>{day_yes_or_no}<div class="line_in_table_week">{line}</div></div></a>""")
    sunday = week_line[0]
    week_line.remove(sunday)
    week_line.append(sunday)
    return week_line
