from django import forms
from .models import StudentRequest, Subject  # Import both models

class StudentRequestForm(forms.ModelForm):
    class Meta:
        model = StudentRequest
        fields = ['student_name', 'phone_number', 'subject', 'attachment']
    
    student_name = forms.CharField(required=True)  # Make student_name required
    phone_number = forms.CharField(required=True)  # Make phone_number required

    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes
        label="Subjects",
        required=True  # Make subject required
    )
    
    attachment = forms.FileField(
        label='Attachment (Image)',
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        required=True  # Make attachment required
    )

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'price', 'image']  # Include all subject fields