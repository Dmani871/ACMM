# Generated by Django 2.1.5 on 2021-02-21 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship', '0010_auto_20210221_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentorprofile',
            name='occupation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
