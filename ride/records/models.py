from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Services(models.Model):
    name_project = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    low_time = models.TimeField()
    high_time = models.TimeField()
    low_duration = models.TimeField()
    high_duration = models.TimeField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    contact = models.TextField(max_length=200, blank=True, null=True)


class Records(models.Model):
    project = models.ForeignKey(Services, on_delete=models.CASCADE)
    date_start = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    driver = models.ForeignKey(User, on_delete=models.CASCADE)

