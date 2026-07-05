from django.contrib.auth.models import AbstractUser
from django.db import models
from django_jalali.db import models as jmodels
from .utils import jalali_now


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    REQUIRED_FIELDS = ["email", "first_name"]
    created_at = jmodels.jDateTimeField(default=jalali_now)

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