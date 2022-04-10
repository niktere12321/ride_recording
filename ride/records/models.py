from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Records(models.Model):
    date_start = models.DateField()
    start_int = models.IntegerField()
    end_int = models.IntegerField()
    driver = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_html_url(self):
        return f'{self.start_int}-{self.end_int}:{self.driver}'


class Records_ship(models.Model):
    date_start = models.DateField()
    start_int = models.IntegerField()
    end_int = models.IntegerField()
    driver = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def get_html_url(self):
        return f'{self.start_int}-{self.end_int}:{self.driver}'
