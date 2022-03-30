from django.contrib import admin

from .models import Records, Records_ship


class RecordsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'date_start',
        'start_time',
        'end_time',
        'driver',
    )


class Records_shipAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'date_start',
        'start_time',
        'end_time',
        'driver',
    )


admin.site.register(Records, RecordsAdmin)
admin.site.register(Records_ship, Records_shipAdmin)
