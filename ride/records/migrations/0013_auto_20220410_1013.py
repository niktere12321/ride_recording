# Generated by Django 2.2.16 on 2022-04-10 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0012_auto_20220410_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='records',
            name='date_end',
        ),
        migrations.RemoveField(
            model_name='records_ship',
            name='date_end',
        ),
    ]
