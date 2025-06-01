from django.contrib import admin
from .models import StudentRequest, Category, Subject
# Register your models here.

admin.site.register((StudentRequest,Category,Subject))