# Generated by Django 4.0.4 on 2022-05-16 17:28

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_cryptography.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenteeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', django_cryptography.fields.encrypt(models.EmailField(max_length=254))),
                ('first_name', django_cryptography.fields.encrypt(models.CharField(max_length=30))),
                ('last_name', django_cryptography.fields.encrypt(models.CharField(max_length=130))),
                ('sex', django_cryptography.fields.encrypt(models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1))),
                ('year_applied', models.CharField(choices=[('A2', 'A level/IB'), ('GRAD', 'Graduate')], max_length=10)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('hear_about_us', models.CharField(choices=[('WM', 'Word of mouth'), ('C', 'Contact from ACMM team'), ('SM', 'Social Media'), ('SU', 'School/University'), ('O', 'Other')], default=None, max_length=10)),
                ('entrance_exam_experience', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('BMAT', 'BMAT'), ('UCAT', 'UCAT'), ('GAMSAT', 'GAMSAT')], max_length=10), default=list, size=None)),
                ('interview_experience', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('P', 'Panel'), ('M', 'MMI'), ('G', 'Group')], max_length=10), size=None)),
                ('area_of_support', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('PS', 'Personal Statement'), ('I', 'Interview'), ('EE', 'Entrance Exam'), ('WE', 'Work Experience')], max_length=10), default=list, size=None)),
                ('mentor_need', models.TextField(blank=True, null=True)),
                ('mentor_help', models.TextField(blank=True, null=True)),
                ('mentor_relationship', models.TextField(blank=True, null=True)),
                ('course', models.CharField(choices=[('M', 'Medicine'), ('D', 'Dentistry')], max_length=10)),
                ('current_application', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True)),
                ('accepted', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MentorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', django_cryptography.fields.encrypt(models.EmailField(max_length=254))),
                ('first_name', django_cryptography.fields.encrypt(models.CharField(max_length=30))),
                ('last_name', django_cryptography.fields.encrypt(models.CharField(max_length=130))),
                ('sex', django_cryptography.fields.encrypt(models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1))),
                ('year_applied', models.CharField(choices=[('A2', 'A level/IB'), ('GRAD', 'Graduate')], max_length=10)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('hear_about_us', models.CharField(choices=[('WM', 'Word of mouth'), ('C', 'Contact from ACMM team'), ('SM', 'Social Media'), ('SU', 'School/University'), ('O', 'Other')], default=None, max_length=10)),
                ('entrance_exam_experience', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('BMAT', 'BMAT'), ('UCAT', 'UCAT'), ('GAMSAT', 'GAMSAT')], max_length=10), default=list, size=None)),
                ('interview_experience', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('P', 'Panel'), ('M', 'MMI'), ('G', 'Group')], max_length=10), size=None)),
                ('area_of_support', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('PS', 'Personal Statement'), ('I', 'Interview'), ('EE', 'Entrance Exam'), ('WE', 'Work Experience')], max_length=10), default=list, size=None)),
                ('occupation', models.CharField(choices=[('MD', 'Doctor'), ('D', 'Dentist'), ('MS', 'Medical Student'), ('DS', 'Dental Student')], max_length=10)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MentorQualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('education_level', models.CharField(choices=[('A2', 'A Level'), ('AS', 'A/S Level'), ('IB', 'International Baccalaureate'), ('SH', 'Scottish Highers and Advanced Highers'), ('UG', 'Undergraduate'), ('M', 'Masters'), ('D', 'Doctorate')], max_length=10)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.mentorprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MenteeQualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('education_level', models.CharField(choices=[('A2', 'A Level'), ('AS', 'A/S Level'), ('IB', 'International Baccalaureate'), ('SH', 'Scottish Highers and Advanced Highers'), ('UG', 'Undergraduate'), ('M', 'Masters'), ('D', 'Doctorate')], max_length=10)),
                ('grade', models.CharField(choices=[('A*', 'A*'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('1st', '1st'), ('2:1', '2:1'), ('2:2', '2:2'), ('3rd', '3rd')], max_length=10)),
                ('predicted', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentorship.menteeprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='menteeprofile',
            name='mentor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentorship.mentorprofile'),
        ),
    ]