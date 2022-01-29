from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()

Car_park = (('квадроцикл', 'atv'), ('лодка', 'boat'))


class Records(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    car_or_ship = models.CharField(max_length=10, choices=Car_park)

    @property
    def get_html_url(self):
        url = reverse('records:records_edit', args=(self.id,))
        return f'<a href="{url}">{self.start_time}</a>'
