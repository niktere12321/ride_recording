# Generated by Django 2.2.16 on 2022-01-30 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0008_auto_20220129_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='car_or_ship',
            field=models.CharField(choices=[('квадроцикл', 'квадроцикл'), ('лодка', 'лодка')], max_length=10),
        ),
    ]