from django.urls import path
from .views import login_view, student_page, admin_page , register_view , logout_view, add_subject
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', login_view, name='login'),
    path('', student_page, name='student_page'),
    path('admin-page/', admin_page, name='admin_page'),
    path('add-subject/', add_subject, name='add_subject'),
    path('register/',   register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)