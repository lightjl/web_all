# Generated by Django 2.0 on 2018-01-14 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xjgl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nhg',
            name='setDate',
            field=models.DateField(auto_now=True),
        ),
    ]
