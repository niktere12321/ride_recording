# Generated by Django 2.2.16 on 2022-01-29 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_auto_20220129_1043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='records',
            old_name='end_date',
            new_name='start_time',
        ),
        migrations.AddField(
            model_name='records',
            name='end_time',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='records',
            name='start_date',
            field=models.DateField(),
        ),
    ]