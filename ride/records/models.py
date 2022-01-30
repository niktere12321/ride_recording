from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

Car_park = (('квадроцикл', 'квадроцикл'), ('лодка', 'лодка'))


class Records(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    car_or_ship = models.CharField(max_length=10, choices=Car_park)

    @property
    def get_html_url(self):
        str_time1 = str(self.start_time)
        tme1 = str_time1[11:16]
        str_time2 = str(self.end_time)
        tme2 = str_time2[11:16]
        return f'{tme1}-{tme2}:{self.driver}-{self.car_or_ship}'

#url = reverse('records:records_edit', args=(self.id,))
