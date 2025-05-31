from django import forms
from .models import StudentRequest, Subject, Category  # Import both models

class StudentRequestForm(forms.ModelForm):
    class Meta:
        model = StudentRequest
        fields = ['student_name', 'univ_id', 'email', 'phone_number', 'subject', 'attachment']

    student_name = forms.CharField(required=True)  # Make student_name required
    univ_id = forms.CharField(required=True)  # Make univ_id required
    email = forms.EmailField(required=True)  # Make email required
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
        fields = ['name', 'price', 'advance_payment', 'image'] 
        
    name = forms.CharField(required=True)
    price = forms.DecimalField(required=True, max_digits=10, decimal_places=2)  
    advance_payment = forms.DecimalField(required=True, max_digits=10, decimal_places=2) 
    image = forms.ImageField(required=True)
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  # Include the name field
