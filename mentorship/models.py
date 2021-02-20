from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField



class UserManager(BaseUserManager):
    def create_user(
            self, email, first_name, last_name, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    
    is_admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as staff. '
        ),
    )

    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True



class MentorProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="user_profile",)
    OCCUPATION_CHOICES = [
    ('Doctor', 'Doctor'),
    ('Dentist', 'Dentist'),
    ('Medical Student', 'Medical Student'),
    ('Graduate Medical Student', 'Graduate Medical Student'),
    ('Medical Student Studying Abroad', 'Medical Student Studying Abroad'),
    ('Dental student', 'Dental student')]
    INTREST_CHOICES = [
    ('Outreach Programmes', 'Outreach Programmes'),
    ('Speaking at events', 'Speaking at events'),
    ('Support for events', 'Support for events'),
    ('Provision of work experience/volunteering opportunities', 'Provision of work experience/volunteering opportunities'),
    ('Additional guidance for mentors (one off)', 'Additional guidance for mentors (one off)')]

    HEAR_ABOUT_US_CHOICES = [
    ('Word of mouth', 'Outreach Programmes'),
    ('Contact from ACMM team', 'Speaking at events'),
    ('Social Media', 'Support for events'),
    ('Provision of work experience/volunteering opportunities', 'Provision of work experience/volunteering opportunities'),
    ('Additional guidance for mentors (one off)', 'Additional guidance for mentors (one off)')]

    current_occupation= models.CharField(max_length=100, default='Doctor', choices=OCCUPATION_CHOICES)
    intrests= MultiSelectField(choices=INTREST_CHOICES)
    specialty= models.CharField(max_length=100, default='N/A')
    location  = CountryField(blank_label='(select country)',default='N/A')
    year_of_study = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    hear_about_us= models.CharField(max_length=100, default='Word of mouth', choices=INTREST_CHOICES)
    hear_about_us_other= models.CharField(max_length=100, default='N/A')
    
    
    is_mentor = models.BooleanField(
        _('mentor status'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as a mentor.'
        ),
    )
    def __str__(self):  # __unicode__ for Python 2
        return self.user.email

class MenteeProfile(models.Model):
    INTERVIEW_EXPERIENCE_CHOICES = [
    ('Panel', 'Panel'),
    ('MMI', 'MMI'),
    ('Group', 'Group')]

    YEAR_APPlIED_CHOICES = [
    ('A level', 'A level'),
    ('International Baccalaureate', 'International Baccalaureate'),
    ('Graduate', 'Graduate')]


    ENTRANCE_EXAM_CHOICES = [
    ('BMAT', 'BMAT'),
    ('UKCAT', 'UKCAT'),
    ('GAMSAT', 'GAMSAT')]
    COUSRSE_CHOICES = [
    ('Medicine', 'Medicine'),
    ('Graduate Medicine', 'Graduate Medicine'),
    ('Dentistry', 'Dentistry')]

    email = models.EmailField(
        verbose_name=_("Mentee's email address"), max_length=255, unique=True,primary_key=True
    )
    first_name = models.CharField("Mentee's first name", max_length=30)
    last_name = models.CharField("Mentee's last name", max_length=30)
    entrance_exam_experience=MultiSelectField(choices=ENTRANCE_EXAM_CHOICES)
    interview_experience=MultiSelectField(choices=INTERVIEW_EXPERIENCE_CHOICES)
    year_applied=models.CharField(max_length=100, default='A level', choices=YEAR_APPlIED_CHOICES)
    subjects = models.CharField(max_length=1024,blank=True)
    universities=models.CharField(max_length=1024,blank=True)
    course=models.CharField(max_length=100, default='Medicine', choices=YEAR_APPlIED_CHOICES)
    applied_this_year = models.BooleanField(
        _('applied this year status'),
        default=True)
    assigned_mentor=models.OneToOneField(MentorProfile, on_delete=models.SET_NULL,null=True,blank=True)
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )
    