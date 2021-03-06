from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=150)
    
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
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile",)
    occupation= models.CharField(max_length=255,blank = True,null = True)
    interests= ArrayField(
        models.CharField(max_length=255, blank=True),
        blank = True,
        null = True,
        )
    specialty= models.CharField(max_length=255, blank = True,null = True)
    
    year_of_study = models.PositiveIntegerField(blank = True,null = True)
    hear_about_us= models.CharField(max_length=255,blank = True,null = True)
    is_mentor = models.BooleanField(
        _('mentor status'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as a mentor.'
        ),
    )
    entrance_exam_experience=ArrayField(
        models.CharField(max_length=100, blank=True),
        blank = True,
        null = True,
        )
    interview_experience=ArrayField(
        models.CharField(max_length=100, blank=True),
        blank = True,
        null = True,
        )
    year_applied=models.CharField(max_length=255,blank = True,null = True)
    def __str__(self):  # __unicode__ for Python 2
        return self.user.email

class MenteeProfile(models.Model):
    email = models.EmailField(
        verbose_name=_("Mentee's email address"), max_length=255, unique=True,primary_key=True
    )
    first_name = models.CharField("First name", max_length=30)
    last_name = models.CharField("Last name", max_length=30)
    entrance_exam=ArrayField(
        models.CharField(max_length=100, blank=True),
        blank = True,
        null = True,
        )
    course = models.CharField(max_length=255, default='Medicine')
    help_needed=models.CharField(max_length=255, blank = True,null = True)
    preparation=models.TextField(null=True, blank=True)
    confidence = models.PositiveIntegerField(default =1 )
    applied_this_year = models.BooleanField(
        _('applied this year status'),
        default=True)
    assigned_mentor=models.OneToOneField(MentorProfile, on_delete=models.SET_NULL,null=True,blank=True,related_name="mentee")
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )
    

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        MentorProfile.objects.create(user=instance)
        instance.profile.save()
