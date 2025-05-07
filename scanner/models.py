from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Ensure you include username when creating a superuser

    class Meta:
        app_label = 'scanner'
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'

    def __str__(self):
        return self.email


# ScanRecord Model
class ScanRecord(models.Model):
    ip = models.GenericIPAddressField()
    scan_type = models.CharField(max_length=50)
    output = models.TextField(blank=True)
    xml_file = models.FileField(upload_to='scans/xml/', null=True)
    html_file = models.FileField(upload_to='scans/html/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='scans'
    )

    class Meta:
        db_table = 'scanner_scanrecord'
        ordering = ['-created_at']  # Example ordering by most recent first

    def __str__(self):
        return f"{self.ip} ({self.scan_type})"


# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    send_copy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Contact Message from {self.name}'
