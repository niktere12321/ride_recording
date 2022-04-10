from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Records(models.Model):
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    driver = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_html_url(self):
        return f'{self.start_time}-{self.end_time}:{self.driver}'


class Records_ship(models.Model):
    date_start = models.DateField(blank=True, null=True)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    driver = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_html_url(self):
        return f'{self.start_time}-{self.end_time}:{self.driver}'
