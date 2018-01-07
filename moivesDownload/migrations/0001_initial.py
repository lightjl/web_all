# Generated by Django 2.0 on 2018-01-07 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Moive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_Zh', models.CharField(max_length=30)),
                ('name_En', models.CharField(max_length=100)),
                ('downloadLink', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Statue_dm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statue', models.CharField(max_length=5)),
                ('means', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moivesDownload.Moive')),
                ('people', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moivesDownload.People')),
                ('statue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moivesDownload.Statue_dm')),
            ],
        ),
    ]
