from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from .forms import StudentRequestForm , SubjectForm
from .models import StudentRequest, Subject
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



def student_page(request):
    if request.method == 'POST':
        form = StudentRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Request submitted successfully!')  # Use messages framework
            return redirect('student_page')  
    else:
        form = StudentRequestForm()

    return render(request, 'accounts/student_page.html', {
        'form': form,
    })


def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)  # Include request.FILES for image uploads
        if form.is_valid():
            form.save()  # Save the subject with the uploaded image
            return redirect('admin_page')  # Redirect after saving
    else:
        form = SubjectForm()
    
    return render(request, 'accounts/add_subject.html', {'form': form})

def submit_request(request):
    if request.method == 'POST':
        form = StudentRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the request to the database
            return redirect('admin_page')  # Redirect to admin page or success page
    else:
        form = StudentRequestForm()
    
    return render(request, 'accounts/submit_request.html', {'form': form})

# def accept_admin(request):
#     accepted_requests = StudentRequest.objects.filter(status='Approved')  # Ensure status matches 'Approved'
#     return render(request, 'accounts/accept_admin.html', {'requests': accepted_requests})

def accept_admin(request):
    accepted_requests = StudentRequest.objects.filter(status='Approved')

    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('done_'):
                request_id = key.split('_')[1]
                done_value = request.POST.get(key) == 'on'
                student_request = StudentRequest.objects.get(id=request_id)
                student_request.done = done_value
                student_request.save()

    return render(request, 'accounts/accept_admin.html', {'requests': accepted_requests})

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