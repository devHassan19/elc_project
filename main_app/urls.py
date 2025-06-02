from django.urls import path
from .views import login_view, student_page, admin_page , register_view , logout_view, add_subject, accept_admin, add_category, delete_subject, update_subject_state, export_selected_fields_excel
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', login_view, name='login'),
    path('', student_page, name='student_page'),
    path('admin-page/', admin_page, name='admin_page'),
    path('add-category/', add_category, name='add_category'),
    path('add-subject/', add_subject, name='add_subject'),
    path('update_subject_state/<int:subject_id>/', update_subject_state, name='update_subject_state'),
    path('subject/delete/<int:subject_id>/', delete_subject, name='delete_subject'),
    path('export_excel/', export_selected_fields_excel, name='export_selected_fields_excel'),
    path('register/',   register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('accepted-requests/', accept_admin, name='accept_admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)