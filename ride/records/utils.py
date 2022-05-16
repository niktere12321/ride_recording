import datetime
import logging
from calendar import HTMLCalendar

import telegram
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse

from .models import Records, Services

TELEGRAM_TOKEN = '2033287598:AAFBPr75b4abzYk0rMSH2Q4ph9mvMmC1U38'
CHAT_ID = '1495697329'

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def send_message(message):
    text = message
    try:
        bot.send_message(CHAT_ID, text)
    except Exception as e:
        logging.error(e, exc_info=True)
        return HttpResponse('Произошла ошибка повторите позже.')


def send_email(to_email, name_project, first_name, last_name, date, start_time, end_time):
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


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, project=None):
        self.year = year
        self.month = month
        self.project = project
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(date_start__day=day)
        services = Services.objects.get(pk=self.project)
        lol_red = f"<div style='height: 30px; width: 10px; background: red; display: table-cell;'> </div>"
        lol_green = f"<div style='height: 30px; width: 10px; background: green; display: table-cell;'> </div>"
        col = []
        for i in range(services.low_time, services.high_time):
            col.append(lol_green)
        for p in events_per_day:
            counter = 0
            for i in range(services.low_time, services.high_time):
                time_i = datetime.datetime.strptime(f"{i}:00:00", "%H:%M:%S")
                time_start = datetime.datetime.strptime(str(p.start_time), "%H:%M:%S")
                time_end = datetime.datetime.strptime(str(p.end_time), "%H:%M:%S")
                if time_i >= time_start and time_i < time_end:
                    col[counter] = lol_red
                counter += 1
        line_1 = f""
        for i in range(len(col)):
            line_1 += col[i]
        color_table = f"<div>{line_1}</div>"
        if day != 0 and day < 10 and self.month < 10:
            return f"<td><a href='{self.project}/records/{ self.year }0{ self.month }0{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span><p>Записи с {services.low_time} до {services.high_time}</p><div style='height: 100px;'>{color_table}</div></a></td>"
        elif day != 0 and day >= 10 and self.month < 10:
            return f"<td><a href='{self.project}/records/{ self.year }0{ self.month }{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span><p>Записи с {services.low_time} до {services.high_time}</p><div style='height: 100px;'>{color_table}</div></a></td>"
        elif day != 0 and day < 10 and self.month >= 10:
            return f"<td><a href='{self.project}/records/{ self.year }{ self.month }0{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span><p>Записи с {services.low_time} до {services.high_time}</p><div style='height: 100px;'>{color_table}</div></a></td>"
        elif day != 0 and day >= 10 and self.month >= 10:
            return f"<td><a href='{self.project}/records/{ self.year }{ self.month }{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span><p>Записи с {services.low_time} до {services.high_time}</p><div style='height: 100px;'>{color_table}</div></a></td>"
        return f"<td></td>"

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        events = Records.objects.filter(date_start__year=self.year, date_start__month=self.month, project=self.project)
        week_day = f'<tr><th> Пн </th><th> Вт </th><th> Ср </th><th> Чт </th><th> Пт </th><th> Сб </th><th> Вс </th></tr>'
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{week_day}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
