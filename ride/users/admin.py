from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    fields = [
        'email',
        'password',
        'role',
        'username',
        'first_name',
        'last_name',
        'active',
        'phone',
    ]
    list_display = (
        'pk',
        'username',
        'email',
        'password',
    )
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
