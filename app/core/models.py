from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)


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
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

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


class PickupPerson(models.Model):
    """Model definition for PickupPerson."""
    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=12, blank=False)

    def __str__(self):
        """Unicode representation of PickupPerson."""
        return self.name


class Parent(models.Model):
    """Model definition for Parent of participant"""
    full_name = models.CharField(max_length=255, blank=False)
    primary_contact_no = models.CharField(max_length=12, blank=False)
    alternate_contact_no = models.CharField(max_length=12, blank=False)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.full_name
