from django import forms
from django.core.exceptions import ValidationError
from .models import StudentRequest, Subject  # Import both models

class StudentRequestForm(forms.ModelForm):
    class Meta:
        model = StudentRequest
        fields = ['student_name', 'phone_number', 'subject', 'attachment']
    
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes
        label="Subjects"
    )
    
    attachment = forms.FileField(
        label='Attachment (Image)',
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        required=False  # Optional if needed
    )
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'price', 'image']  # Include all subject fields