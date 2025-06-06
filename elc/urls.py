"""
URL configuration for elc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('student-page/', views.student_page, name='student_page'),
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('login/', views.login_view, name='login'),
    path('admin-page/', views.admin_page, name='admin_page'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('accepted-requests/', views.accept_admin, name='accept_admin'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)