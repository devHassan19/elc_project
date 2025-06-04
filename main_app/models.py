from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    STATE_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    ]

    name = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Link to Category
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='Draft')  # New state field

    def __str__(self):
        return self.name

class StudentRequest(models.Model):
    student_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=255, null=True)
    univ_id = models.CharField(max_length=20, null=True)
    subject = models.ManyToManyField(Subject)
    attachment = CloudinaryField('file')
    status = models.CharField(max_length=10, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    first_payment = models.BooleanField(default=False)
    second_payment = models.BooleanField(default=False)

    def __str__(self):
        return self.student_name