from django.contrib import admin

from .models import Records, Services


class RecordsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'project',
        'date_start',
        'start_time',
        'end_time',
        'driver',
    )


class ServicesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name_project',
        'description',
        'low_time',
        'high_time',
        'contact',
    )


admin.site.register(Services, ServicesAdmin)
admin.site.register(Records, RecordsAdmin)
