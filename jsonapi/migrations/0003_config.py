# Generated by Django 2.2.4 on 2019-10-16 04:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jsonapi', '0002_auto_20191014_0542'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_date', models.DateField(default=datetime.date(2019, 10, 16))),
                ('ending_date', models.DateField(default=datetime.date(2020, 1, 8))),
            ],
        ),
    ]