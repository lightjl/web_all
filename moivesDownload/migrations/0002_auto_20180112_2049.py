# Generated by Django 2.0 on 2018-01-12 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moivesDownload', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statue_dm',
            name='statue',
        ),
        migrations.AddField(
            model_name='statue_dm',
            name='leave',
            field=models.CharField(default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='statue_dm',
            name='show',
            field=models.BooleanField(default=1),
        ),
    ]
