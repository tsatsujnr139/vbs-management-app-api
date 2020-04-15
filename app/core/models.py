from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)

from enum import Enum


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves a new user"""
        if not email:
            raise ValueError("Email is a required field")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """creates and saves a new superuser"""
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model with email as primary identifier"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(default=now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Grade(models.Model):
    """Model definition for Grade."""
    name = models.CharField(max_length=100, unique=True, blank=False)

    def __str__(self):
        """Unicode representation of Grade."""
        return self.name


class Church(models.Model):
    """Model definition for Church."""
    name = models.CharField(max_length=255, unique=True, blank=False)

    def __str__(self):
        """Unicode representation of Church."""
        return self.name


class GenderChoice(Enum):
    MALE = 'Male'
    FEMALE = 'Female'


class Participant(models.Model):
    """Model definition for Participant model"""
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    gender = models.CharField(max_length=6)
    medical_info = models.TextField(blank=True)
    date_of_birth = models.DateField(default=now)
    grade = models.CharField(max_length=10, blank=False)
    parent_name = models.CharField(max_length=100, blank=False)
    primary_contact_no = models.CharField(max_length=12, blank=False)
    alternate_contact_no = models.CharField(max_length=12, blank=False)
    email = models.EmailField(max_length=100, blank=True)
    church = models.CharField(max_length=150, blank=False)
    pickup_person_name = models.CharField(max_length=100)
    pickup_person_contact_no = models.CharField(max_length=12, blank=False)
    created = models.DateTimeField(default=now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Volunteer(models.Model):
    """Model definition for volunteer"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6)
    preferred_role = models.CharField(max_length=12)
    church = models.CharField(max_length=150, blank=False)
    preferred_class = models.CharField(max_length=10, blank=False)
    contact_no = models.CharField(max_length=12, blank=False)
    whatsApp_no = models.CharField(max_length=12, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    previous_volunteer = models.BooleanField(default=False)
    previous_site = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
