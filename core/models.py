from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django_jalali.db import models as jmodels
from .utils import jalali_now

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('وارد کردن ایمیل الزامی است.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name"]
    created_at = jmodels.jDateTimeField(default=jalali_now)
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.first_name})"


class Note(models.Model):
    NOTE_TYPE_CHOICES = [
        ("note", "یادداشت"),
        ("reminder", "یادآوری"),
    ]
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notes"
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    note_type = models.CharField(
        max_length=10,
        choices=NOTE_TYPE_CHOICES,
        default="note",
        blank=False,
        null=False,
    )
    created_at = jmodels.jDateTimeField(default=jalali_now)

    def __str__(self):
        return f"{self.title}"