# Generated by Django 2.1.5 on 2021-02-21 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship', '0005_auto_20210221_1105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mentorprofile',
            old_name='intrests',
            new_name='interests',
        ),
    ]
