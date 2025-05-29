from django.db import models
from django.utils import timezone

class Subject(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='subject_images/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Set default value here
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class StudentRequest(models.Model):
    student_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    subject = models.ManyToManyField(Subject)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    status = models.CharField(max_length=10, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)  # Ensure this field exists

    def __str__(self):
        return self.student_name