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
		lol_red = f"<span style='outline: 2px solid #000; font-size: 18px; color: red; background-color: red'> --- </span>"
		lol_green = f"<span style='outline: 2px solid #000; font-size: 18px; color: green; background-color: green'> --- </span>"
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
			d += f'<li> {event.get_html_url} </li>'
		line_1 = f"{a1}{a2}{a3}{a4}"
		line_2 = f"{b1}{b2}{b3}{b4}"
		line_3 = f"{c1}{c2}{c3}{c4}"
		color_table = f"<span>{line_1}</span><br><span>{line_2}</span><br><span>{line_3}</span>"
		if day != 0 and day < 10 and self.month < 10:
			return f"<td><a href='records/{ self.year }0{ self.month }0{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span><p>Записи</p><div style='height: 100px; background-color: white'>{color_table} </div></a></td>"
		elif day != 0 and day >= 10 and self.month < 10:
			return f"<td><a href='records/{ self.year }0{ self.month }{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span><p>Записи</p><div style='height: 100px; background-color: white'>{color_table} </div></a></td>"
		elif day != 0 and day < 10 and self.month > 10:
			return f"<td><a href='records/{ self.year }{ self.month }0{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span><p>Записи</p><div style='height: 100px; background-color: white'>{color_table} </div></a></td>"
		return '<td></td>'

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
		lol_red = f"<span style='outline: 2px solid #000; font-size: 18px; color: red; background-color: red'> --- </span>"
		lol_green = f"<span style='outline: 2px solid #000; font-size: 18px; color: green; background-color: green'> --- </span>"
		a11 = lol_green
		a22 = lol_green
		a33 = lol_green
		a44 = lol_green
		b11 = lol_green
		b22 = lol_green
		b33 = lol_green
		b44 = lol_green
		c11 = lol_green
		c22 = lol_green
		c33 = lol_green
		c44 = lol_green
		for event_ship in events_per_day_ship:
			for i in range(6, 19):
				if i == 6 and i >= event_ship.start_time and i < event_ship.end_time:
					a11 = lol_red
				elif i == 7 and i >= event_ship.start_time and i < event_ship.end_time:
					a22 = lol_red
				elif i == 8 and i >= event_ship.start_time and i < event_ship.end_time:
					a33 = lol_red
				elif i == 9 and i >= event_ship.start_time and i < event_ship.end_time:
					a44 = lol_red
				elif i == 10 and i >= event_ship.start_time and i < event_ship.end_time:
					b11 = lol_red
				elif i == 11 and i >= event_ship.start_time and i < event_ship.end_time:
					b22 = lol_red
				elif i == 12 and i >= event_ship.start_time and i < event_ship.end_time:
					b33 = lol_red
				elif i == 13 and i >= event_ship.start_time and i < event_ship.end_time:
					b44 = lol_red
				elif i == 14 and i >= event_ship.start_time and i < event_ship.end_time:
					c11 = lol_red
				elif i == 15 and i >= event_ship.start_time and i < event_ship.end_time:
					c22 = lol_red
				elif i == 16 and i >= event_ship.start_time and i < event_ship.end_time:
					c33 = lol_red
				elif i == 17 and i >= event_ship.start_time and i < event_ship.end_time:
					c44 = lol_red
		line_11 = f"{a11}{a22}{a33}{a44}"
		line_22 = f"{b11}{b22}{b33}{b44}"
		line_33 = f"{c11}{c22}{c33}{c44}"
		color_table1 = f"<span>{line_11}</span><br><span>{line_22}</span><br><span>{line_33}</span>"
		if day != 0 and day < 10 and self.month < 10:
			return f"<td><a href='records_ship/{ self.year }0{ self.month }0{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span><p>Записи</p><div style='height: 100px; background-color: white'{color_table1} </div></a></td>"
		elif day != 0 and day >= 10 and self.month < 10:
			return f"<td><a href='records_ship/{ self.year }0{ self.month }{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span><p>Записи</p><div style='height: 100px; background-color: white'{color_table1} </div></a></td>"
		elif day != 0 and day < 10 and self.month > 10:
			return f"<td><a href='records_ship/{ self.year }{ self.month }0{ day }/'> <span class='date' style='position: relative; bottom: 20px;'>{day}</span><p>Записи</p><div style='height: 100px; background-color: white'{color_table1} </div></a></td>"
		return '<td></td>'

#d += f'<li> {event_ship.get_html_url} </li>'

	def formatweek(self, theweek, events_ship):
		week1 = ''
		for d, weekday in theweek:
			week1 += self.formatday(d, events_ship)
		return f'<tr> {week1} </tr>'

	def formatmonth(self, withyear=True):
		events_ship = Records_ship.objects.filter(date_start__year=self.year, date_start__month=self.month)
		cal1 = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal1 += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal1 += f'{self.formatweekheader()}\n'
		for week1 in self.monthdays2calendar(self.year, self.month):
			cal1 += f'{self.formatweek(week1, events_ship)}\n'
		return cal1
