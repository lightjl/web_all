# Generated by Django 2.0 on 2018-01-13 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_rask_weekday'),
        ('followXS', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xs',
            name='name',
        ),
        migrations.AddField(
            model_name='xs',
            name='rask',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='control.Rask'),
            preserve_default=False,
        ),
    ]