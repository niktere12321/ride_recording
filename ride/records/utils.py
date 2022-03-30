from calendar import HTMLCalendar

from .models import Records, Records_ship


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	def formatday(self, day, events):
		events_per_day = events.filter(date_start__day=day)
		d = ''
		lol_red = f"<span style='margin: 0; border: 0; padding: 0; font-size: 18px; color: red; background-color: red'> --- </span>"
		lol_green = f"<span style='margin: 0; border: 0; padding: 0; font-size: 18px; color: green; background-color: green'> --- </span>"
		a1 = ''
		a2 = ''
		a3 = ''
		a4 = ''
		b1 = ''
		b2 = ''
		b3 = ''
		b4 = ''
		c1 = ''
		c2 = ''
		c3 = ''
		c4 = ''
		for event in events_per_day:
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
				elif i == 6 and not (i >= event.start_time and i < event.end_time) and a1 != lol_red:
					a1 = lol_green
				elif i == 7 and not (i >= event.start_time and i < event.end_time) and a2 != lol_red:
					a2 = lol_green
				elif i == 8 and not (i >= event.start_time and i < event.end_time) and a3 != lol_red:
					a3 = lol_green
				elif i == 9 and not (i >= event.start_time and i < event.end_time) and a4 != lol_red:
					a4 = lol_green
				elif i == 10 and not (i >= event.start_time and i < event.end_time) and b1 != lol_red:
					b1 = lol_green
				elif i == 11 and not (i >= event.start_time and i < event.end_time) and b2 != lol_red:
					b2 = lol_green
				elif i == 12 and not (i >= event.start_time and i < event.end_time) and b3 != lol_red:
					b3 = lol_green
				elif i == 13 and not (i >= event.start_time and i < event.end_time) and b4 != lol_red:
					b4 = lol_green
				elif i == 14 and not (i >= event.start_time and i < event.end_time) and c1 != lol_red:
					c1 = lol_green
				elif i == 15 and not (i >= event.start_time and i < event.end_time) and c2 != lol_red:
					c2 = lol_green
				elif i == 16 and not (i >= event.start_time and i < event.end_time) and c3 != lol_red:
					c3 = lol_green
				elif i == 17 and not (i >= event.start_time and i < event.end_time) and c4 != lol_red:
					c4 = lol_green
			d += f'<li> {event.get_html_url} </li>'
		line_1 = f"{a1}{a2}{a3}{a4}"
		line_2 = f"{b1}{b2}{b3}{b4}"
		line_3 = f"{c1}{c2}{c3}{c4}"
		color_table = f"<span style='margin: 0; border: 0; padding: 0;'>{line_1}</span><br><span style='margin: 0; border: 0; padding: 0;'>{line_2}</span><br><span style='margin: 0; border: 0; padding: 0;'>{line_3}</span>"
		if day != 0 and day < 10 and self.month < 10:
			return f"<td><a href='records/{ self.year }0{ self.month }0{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span><div style='margin: 0; border: 0; padding: 0; height: 100px; background-color: blue'{color_table} </div></a></td>"
		elif day != 0 and day >= 10 and self.month < 10:
			return f"<td><a href='records/{ self.year }0{ self.month }{ day }/'> <span class='date'>{day}</span><ul> {d} </ul></a></td>"
		elif day != 0 and day < 10 and self.month > 10:
			return f"<td><a href='records/{ self.year }{ self.month }0{ day }/'> <span class='date'>{day}</span><ul> {d} </ul></a></td>"
		return '<td></td>'
#<table style='width: 50px; height: 100%;'><tbody><tr><td>lol</td><td>pop</td></tr><tr><td>ala</td><td>olo</td></tr></tbody></table>
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	def formatmonth(self, withyear=True):
		events = Records.objects.filter(date_start__year=self.year, date_start__month=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal


class Calendar_ship(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar_ship, self).__init__()

	def formatday(self, day, events_ship):
		events_per_day_ship = events_ship.filter(date_start__day=day)
		d = ''
		for event_ship in events_per_day_ship:
			d += f'<li> {event_ship.get_html_url} </li>'
		if day != 0 and day < 10 and self.month < 10:
			return f"<td><a href='records_ship/{ self.year }0{ self.month }0{ day }/'> <span class='date'>{day}</span><ul> {d} </ul></a></td>"
		elif day != 0 and day >= 10 and self.month < 10:
			return f"<td><a href='records_ship/{ self.year }0{ self.month }{ day }/'> <span class='date'>{day}</span><ul> {d} </ul></a></td>"
		elif day != 0 and day < 10 and self.month > 10:
			return f"<td><a href='records_ship/{ self.year }{ self.month }0{ day }/'> <span class='date'>{day}</span><ul> {d} </ul></a></td>"
		return '<td></td>'

	def formatweek(self, theweek, events_ship):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events_ship)
		return f'<tr> {week} </tr>'

	def formatmonth(self, withyear=True):
		events_ship = Records_ship.objects.filter(date_start__year=self.year, date_start__month=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events_ship)}\n'
		return cal
