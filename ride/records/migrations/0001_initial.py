# Generated by Django 2.2.16 on 2022-05-16 18:49

from django.conf import settings
import django.core.validators
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
                ('description', models.TextField(max_length=200)),
                ('low_time', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)])),
                ('high_time', models.IntegerField(default=24, validators=[django.core.validators.MaxValueValidator(24), django.core.validators.MinValueValidator(4)])),
                ('low_duration', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(24), django.core.validators.MinValueValidator(1)])),
                ('high_duration', models.IntegerField(default=24, validators=[django.core.validators.MaxValueValidator(24), django.core.validators.MinValueValidator(1)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('contact', models.TextField(max_length=200)),
            ],
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
        ),
    ]
