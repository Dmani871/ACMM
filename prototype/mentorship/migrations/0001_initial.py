# Generated by Django 2.1.5 on 2021-02-21 03:03

from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether this user should be treated as staff. ', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MenteeProfile',
            fields=[
                ('email', models.EmailField(max_length=255, primary_key=True, serialize=False, unique=True, verbose_name="Mentee's email address")),
                ('first_name', models.CharField(max_length=30, verbose_name="Mentee's first name")),
                ('last_name', models.CharField(max_length=30, verbose_name="Mentee's last name")),
                ('entrance_exam_experience', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), blank=True, null=True, size=None)),
                ('interview_experience', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), blank=True, null=True, size=None)),
                ('year_applied', models.CharField(choices=[('A level', 'A level'), ('International Baccalaureate', 'International Baccalaureate'), ('Graduate', 'Graduate')], default='A level', max_length=100)),
                ('subjects', django.contrib.postgres.fields.ArrayField(base_field=multiselectfield.db.fields.MultiSelectField(choices=[('Panel', 'Panel'), ('MMI', 'MMI'), ('Group', 'Group')], max_length=15), size=None)),
                ('universities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), blank=True, null=True, size=None)),
                ('course', models.CharField(choices=[('A level', 'A level'), ('International Baccalaureate', 'International Baccalaureate'), ('Graduate', 'Graduate')], default='Medicine', max_length=100)),
                ('applied_this_year', models.BooleanField(default=True, verbose_name='applied this year status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
        ),
        migrations.CreateModel(
            name='MentorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation', models.CharField(default='Doctor', max_length=255)),
                ('intrests', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), blank=True, null=True, size=None)),
                ('specialty', models.CharField(default='N/A', max_length=100)),
                ('location', django_countries.fields.CountryField(default='N/A', max_length=2)),
                ('year_of_study', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('hear_about_us', models.CharField(choices=[('Outreach Programmes', 'Outreach Programmes'), ('Speaking at events', 'Speaking at events'), ('Support for events', 'Support for events'), ('Provision of work experience/volunteering opportunities', 'Provision of work experience/volunteering opportunities'), ('Additional guidance for mentors (one off)', 'Additional guidance for mentors (one off)')], default='Word of mouth', max_length=100)),
                ('hear_about_us_other', models.CharField(default='N/A', max_length=100)),
                ('is_mentor', models.BooleanField(default=True, help_text='Designates whether this user should be treated as a mentor.', verbose_name='mentor status')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='menteeprofile',
            name='assigned_mentor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentorship.MentorProfile'),
        ),
    ]