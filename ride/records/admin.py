from django.contrib import admin

from .models import Records


class RecordsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'start_date',
        'end_date',
        'driver',
        'car_or_ship'
    )


admin.site.register(Records, RecordsAdmin)
