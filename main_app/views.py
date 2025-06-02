from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from .forms import StudentRequestForm , SubjectForm, CategoryForm
from .models import StudentRequest, Subject, Category
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user_type = form.cleaned_data.get("user_type")

            user = User.objects.create_user(username=username, password=password)

            user.is_staff = user_type == 'staff'
            user.save()

           
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()
        
    return render(request, 'accounts/register.html', {'form': form})
            
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin-page/')
            elif user.is_staff:
                return redirect('/staff-page/')
            else:
                return redirect('/')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

# def student_page(request):
#     subjects = Subject.objects.all()  # Fetch all subjects

#     if request.method == 'POST':
#         form = StudentRequestForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request,  'تم تقديم طلبك بنجاح. سيتم التواصل معك خلال 24 ساعة. إذا لم تصلك رسالتنا، الرجاء التواصل مع الدعم الفني  36195555. \nRequest submitted successfully! We will contact you within 24 hours. If you do not receive our message, please contact ELC support.')
#             return redirect('student_page')
#     else:
#         form = StudentRequestForm()  # Use empty form for GET request

#     return render(request, 'accounts/student_page.html', {
#         'form': form,
#         'subjects': subjects,
#     })

def student_page(request):
    # Fetch only subjects that are published
    subjects = Subject.objects.filter(state='Published')  

    if request.method == 'POST':
        form = StudentRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تقديم طلبك بنجاح. سيتم التواصل معك خلال 24 ساعة. إذا لم تصلك رسالتنا، الرجاء التواصل مع الدعم الفني 36195555. \nRequest submitted successfully! We will contact you within 24 hours. If you do not receive our message, please contact ELC support.')
            return redirect('student_page')
    else:
        form = StudentRequestForm()  # Use empty form for GET request

    return render(request, 'accounts/student_page.html', {
        'form': form,
        'subjects': subjects,
    })

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Category Add successfully!') 
            return redirect('add_category')  # Redirect after saving
    else:
        form = CategoryForm()

    return render(request, 'accounts/add_category.html', {'form': form})

def add_subject(request):
    categories = Category.objects.all()  # Fetch all categories
    subjects = Subject.objects.all()  # Fetch all subjects

    # Handle search functionality
    selected_category = request.GET.get('category', '')
    if selected_category:
        subjects = subjects.filter(category_id=selected_category)  # Filter subjects by selected category

    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.save(commit=False)  # Create subject instance but don’t save yet
            
            # Get the category by ID and assign it to the subject
            category_id = request.POST.get('category')
            subject.category = get_object_or_404(Category, id=category_id)  # Fetch the category instance
            
            subject.save()  # Save the subject
            messages.success(request, 'Subject added successfully!')  # Success message
            return redirect('add_subject')  # Redirect after saving
    else:
        form = SubjectForm()

    return render(request, 'accounts/add_subject.html', {
        'form': form,
        'categories': categories,
        'subjects': subjects,
        'selected_category': selected_category,  # Pass the selected category to the template
    })

def update_subject_state(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        new_state = request.POST.get('state')
        if new_state in ['Draft', 'Published', 'Archived']:
            subject.state = new_state  # Update the state
            subject.save()  # Save the changes
            messages.success(request, 'Subject state updated successfully!')  # Success message
        else:
            messages.error(request, 'Invalid state selected.')  # Error message

    return redirect('add_subject') 

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()  # Delete the subject
    messages.success(request, 'Subject deleted successfully!')  # Add success message
    return redirect('add_subject') 

def submit_request(request):
    if request.method == 'POST':
        form = StudentRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the request to the database
            return redirect('admin_page')  # Redirect to admin page or success page
    else:
        form = StudentRequestForm()
    
    return render(request, 'accounts/submit_request.html', {'form': form})
    
def accept_admin(request):
    query = request.GET.get('search', '')
    query_field = request.GET.get('field', 'student_name')  # Default to student_name
    first_payment = request.GET.get('first_payment')  # Check if first_payment is checked
    second_payment = request.GET.get('second_payment')  # Check if second_payment is checked
    accepted_requests = StudentRequest.objects.filter(status='Approved')

    if query:
        if query_field == 'student_name':
            accepted_requests = accepted_requests.filter(student_name__icontains=query)
        elif query_field == 'univ_id':
            accepted_requests = accepted_requests.filter(univ_id__icontains=query)
        elif query_field == 'status':
            accepted_requests = accepted_requests.filter(status__icontains=query)

    # Filter by payment status if checkboxes are checked
    if first_payment and not second_payment:
        accepted_requests = accepted_requests.filter(first_payment=False)
    elif second_payment and not first_payment:
        accepted_requests = accepted_requests.filter(second_payment=False)

    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('first_payment_'):
                request_id = key.split('_')[2]
                payment_value = request.POST.get(key) == 'on'
                student_request = StudentRequest.objects.get(id=request_id)
                student_request.first_payment = payment_value
                student_request.save()
            elif key.startswith('second_payment_'):
                request_id = key.split('_')[2]
                payment_value = request.POST.get(key) == 'on'
                student_request = StudentRequest.objects.get(id=request_id)
                student_request.second_payment = payment_value
                student_request.save()

        # Ensure unchecked checkboxes are set to False
        for request_id in accepted_requests.values_list('id', flat=True):
            if f'first_payment_{request_id}' not in request.POST:
                student_request = StudentRequest.objects.get(id=request_id)
                student_request.first_payment = False
                student_request.save()
            if f'second_payment_{request_id}' not in request.POST:
                student_request = StudentRequest.objects.get(id=request_id)
                student_request.second_payment = False
                student_request.save()

    return render(request, 'accounts/accept_admin.html', {
        'requests': accepted_requests,
        'query': query,
        'query_field': query_field,
        'first_payment': first_payment,
        'second_payment': second_payment
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        request_id = request.POST.get('request_id')
        student_request = get_object_or_404(StudentRequest, id=request_id)
        
        if action == 'approve':
            student_request.status = 'Approved'
            messages.success(request, f'Request for {student_request.student_name} approved.')
        elif action == 'reject':
            student_request.status = 'Rejected'
            messages.error(request, f'Request for {student_request.student_name} rejected.')
        
        student_request.save()

    # Fetch all requests, ordered by creation date
    requests = StudentRequest.objects.all().order_by('-created_at')
    return render(request, 'accounts/admin_page.html', {'requests': requests})


def logout_view(request):
     if request.method == "POST":
         logout(request)
         return redirect('login')
     else:
         return redirect('login')