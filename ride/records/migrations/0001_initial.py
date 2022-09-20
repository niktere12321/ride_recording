# Generated by Django 2.2.16 on 2022-09-20 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_project', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('low_time', models.TimeField()),
                ('high_time', models.TimeField()),
                ('low_duration', models.TimeField()),
                ('high_duration', models.TimeField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('contact', models.TextField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Транспортное средство',
                'verbose_name_plural': 'Транспортные средства',
            },
        ),
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.Services')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
            },
        ),
    ]
