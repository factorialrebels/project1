# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('Meal_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Meal_Category', models.CharField(choices=[(b'BR', b'Breakfast'), (b'LUN', b'Lunch'), (b'DIN', b'Dinner')], default=b'BR', max_length=3)),
                ('Date', models.DateField()),
                ('Meal_No_Tip', models.FloatField()),
                ('Meal_Tip', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Traveler',
            fields=[
                ('SAP_ID', models.BigIntegerField(primary_key=True, serialize=False)),
                ('First_Name', models.CharField(max_length=200)),
                ('Last_Name', models.CharField(max_length=200)),
                ('Title', models.CharField(max_length=200)),
                ('Email', models.CharField(max_length=200)),
                ('Department_Name', models.CharField(max_length=200)),
            ],
        ),
    ]
