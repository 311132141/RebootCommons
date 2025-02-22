from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

# Custom User Manager
class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, company=None, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, company=company, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name=None, email=None, password=None, company=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, company, **extra_fields)

    def create_superuser(self, name=None, email=None, password=None, company=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not name:
            name = "Admin"  # Default name for superuser if not provided
        return self._create_user(name, email, password, company, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, default="Anonymous User")
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    course_type = models.ForeignKey('survey.CourseType', on_delete=models.SET_NULL, blank=True, null=True)
    # programs = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.course_type.name if self.course_type else 'No Course'})"

class CompanyExplanation(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, primary_key=True)
    explanation_text = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Explanation for {self.company.name}"
    
class UserExplanation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    explanation_text = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Explanation for User: {self.user.email}"
