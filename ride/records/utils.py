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


class Calendar(HTMLCalendar):
    """Создание основного календаря"""
    def __init__(self, year=None, month=None, project=None):
        self.year = year
        self.month = month
        self.project = project
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(date_start__day=day)
        services = Services.objects.get(pk=self.project)
        if day != 0:
            date_day = datetime.datetime.strptime(f"{self.year}-{self.month}-{day}", "%Y-%m-%d").date()
        """Получение полоски показывающей загруженость дня"""
        lol_red = f"<div style='height: 30px; width: 10px; background: red; display: table-cell;'> </div>"
        lol_green = f"<div style='height: 30px; width: 10px; background: green; display: table-cell;'> </div>"
        lol_brown = f"<div style='height: 30px; width: 50px; background: #808080; display: table-cell;'> </div>"
        col = []
        for i in range(time_step(services.low_time), time_step(services.high_time)):
            if day != 0 and date_day < datetime.datetime.now().date():
                col.append(lol_brown)
            elif day != 0 and date_day == datetime.datetime.now().date():
                if time_step(datetime.datetime.now().time()) <= i:
                    col.append(lol_green)
                else:
                    col.append(lol_brown)
            else:
                col.append(lol_green)
        for p in events_per_day:
            counter = 0
            for i in range(len(col)):
                time_i = datetime.datetime.strptime(get_time(i, time_step(services.low_time)), "%H:%M:%S")
                time_start = datetime.datetime.strptime(str(p.start_time), "%H:%M:%S")
                time_end = datetime.datetime.strptime(str(p.end_time), "%H:%M:%S")
                if time_i >= time_start and time_i < time_end:
                    col[counter] = lol_red
                counter += 1
        line_1 = f""
        for i in range(len(col)):
            line_1 += col[i]
        color_table = f"<div>{line_1}</div>"
        """Создание Id для дня с изменением цвета"""
        day_color = ''
        date_now = datetime.datetime.strptime(str(datetime.datetime.now().date()), "%Y-%m-%d").date()
        if day != 0:
            if date_day == date_now:
                day_color = "now_day_color"
                day_yes_or_no = f'<p>Записи с {str(datetime.datetime.now().time())[0:5]} до {str(services.high_time)[0:5]}</p>'
            elif date_day <= date_now:
                day_color = "pass_day_color"
                day_yes_or_no = f'<p>Запись недоступна</p>'
            else:
                day_color = "future_day_color"
                day_yes_or_no = f'<p>Записи с {str(services.low_time)[0:5]} до {str(services.high_time)[0:5]}</p>'
        """Создание ячейки дня с ссылкой"""
        if day != 0 and day < 10 and self.month < 10:
            return f"<td id={day_color}><a href='{self.project}/records/{ self.year }0{ self.month }0{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span>{day_yes_or_no }<div style='height: 100px;'>{color_table}</div></a></td>"
        elif day != 0 and day >= 10 and self.month < 10:
            return f"<td id={day_color}><a href='{self.project}/records/{ self.year }0{ self.month }{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span>{day_yes_or_no }<div style='height: 100px;'>{color_table}</div></a></td>"
        elif day != 0 and day < 10 and self.month >= 10:
            return f"<td id={day_color}><a href='{self.project}/records/{ self.year }{ self.month }0{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span>{day_yes_or_no }<div style='height: 100px;'>{color_table}</div></a></td>"
        elif day != 0 and day >= 10 and self.month >= 10:
            return f"<td id={day_color}><a href='{self.project}/records/{ self.year }{ self.month }{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span>{day_yes_or_no }<div style='height: 100px;'>{color_table}</div></a></td>"
        return f"<td></td>"

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        events = Records.objects.filter(date_start__year=self.year, date_start__month=self.month, project=self.project)
        try:
            locale.setlocale(locale.LC_PAPER, 'ru_RU.UTF-8')
        except Exception:
            try:
                locale.setlocale(locale.LC_NAME, 'ru_RU.UTF-8')
            except Exception as e:
                locale.setlocale(locale.LC_ADDRESS, 'ru_RU.UTF-8')
        week_day = f'<tr><th id="border-left"> Пн </th><th> Вт </th><th> Ср </th><th> Чт </th><th> Пт </th><th> Сб </th><th id="border-right"> Вс </th></tr>'
        cal = f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{week_day}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
