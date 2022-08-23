from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


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

    USERNAME_FIELD = "email"


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


MALE = "Male"
FEMALE = "Female"

GENDER_OPTIONS = (
    (MALE, "MALE"),
    (FEMALE, "FEMALE"),
)


class Participant(models.Model):
    """Model definition for Participant model"""

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    gender = models.CharField(max_length=6, choices=GENDER_OPTIONS)
    medical_info = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=False)
    date_of_birth = models.DateField(default=now)
    grade = models.ForeignKey(
        "Grade", to_field="name", on_delete=models.CASCADE
    )
    parent_name = models.CharField(max_length=100, blank=False)
    primary_contact_no = models.CharField(max_length=15, blank=False)
    alternate_contact_no = models.CharField(max_length=15, blank=False)
    whatsApp_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True)
    church = models.CharField(max_length=150, blank=False)
    pickup_person_name = models.CharField(
        max_length=100, blank=True, null=True
    )
    pickup_person_contact_no = models.CharField(
        max_length=12, blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


TEACHING = "Teaching"
TEACHING_ASSISTANT = "Teaching Assistant"
SPECIAL_NEEDS = "Special Needs"
IT = "IT"

VOLUNTEER_ROLE_OPTIONS = (
    (TEACHING, "TEACHING"),
    (TEACHING_ASSISTANT, "TEACHING ASSISTANT"),
    (SPECIAL_NEEDS, "SPECIAL NEEDS"),
    (IT, "IT"),
)


class Volunteer(models.Model):
    """Model definition for volunteer"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_OPTIONS)
    preferred_role = models.CharField(
        max_length=18, choices=VOLUNTEER_ROLE_OPTIONS
    )
    church = models.CharField(max_length=150, blank=False)
    preferred_class = models.CharField(max_length=10, blank=False)
    contact_no = models.CharField(max_length=13, blank=False)
    whatsApp_no = models.CharField(max_length=13, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    previous_volunteer = models.BooleanField(default=False)
    previous_site = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AttendanceType(models.Model):
    """Model definition for supported attendance types"""

    name = models.CharField(max_length=8)
    created = models.DateTimeField(default=now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    """Model definition for the session a participant can opt for"""

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    eligible_grades = models.ManyToManyField("Grade")
    supported_attendance_types = models.ManyToManyField("AttendanceType")
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    created = models.DateTimeField(default=now, editable=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
