from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Services(models.Model):
    name_project = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200)
    low_time = models.IntegerField(default=0, validators=[MaxValueValidator(20), MinValueValidator(0)])
    high_time = models.IntegerField(default=24,  validators=[MaxValueValidator(24), MinValueValidator(4)])
    low_duration = models.IntegerField(default=1,  validators=[MaxValueValidator(24), MinValueValidator(1)])
    high_duration = models.IntegerField(default=24,  validators=[MaxValueValidator(24), MinValueValidator(1)])
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Records(models.Model):
    project = models.ForeignKey(Services, on_delete=models.CASCADE)
    date_start = models.DateField()
    start_time = models.IntegerField(validators=[MaxValueValidator(24), MinValueValidator(0)])
    end_time = models.IntegerField(validators=[MaxValueValidator(24), MinValueValidator(0)])
    driver = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_html_url(self):
        return f'{self.start_time}-{self.end_time}:{self.driver}'
