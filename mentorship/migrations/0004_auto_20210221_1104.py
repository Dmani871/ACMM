# Generated by Django 2.1.5 on 2021-02-21 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship', '0003_auto_20210221_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorprofile',
            name='hear_about_us',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mentorprofile',
            name='year_of_study',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
