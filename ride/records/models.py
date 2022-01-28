from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

Car_park = (('квадроцикл', 'atv'), ('лодка', 'boat'))


class Records(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    car_or_ship = models.CharField(max_length=10, choices=Car_park)
