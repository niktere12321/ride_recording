from calendar import HTMLCalendar

import telegram

from .models import Records, Services

TELEGRAM_TOKEN = '2033287598:AAFBPr75b4abzYk0rMSH2Q4ph9mvMmC1U38'
CHAT_ID = '1495697329'

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def send_message(message):
    text = message
    bot.send_message(CHAT_ID, text)


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
                if i >= p.start_time and i < p.end_time:
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
        week_day = f'<tr><th> Пон </th><th> Вто </th><th> Сре </th><th> Чет </th><th> Пят </th><th> Суб </th><th> Вос </th></tr>'
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{week_day}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
