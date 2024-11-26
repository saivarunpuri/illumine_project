from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Home page URL (renders home.html)
    path('', views.home, name='home'),  # Home page route
    # Authentication URLs
    path('login/', views.user_login, name='login'),  # Login view for both student and teacher
    path('logout/', views.user_logout, name='logout'),  # Logout view

    # Teacher URLs
    path('teacher/dashboard/<int:teacher_id>/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/add-student-mapping/<int:teacher_id>', views.add_student_mapping, name='add_student_mapping'),  # Add student-teacher mapping
    path('teacher/teacher_profile/<int:teacher_id>/', views.teacher_profile, name='teacher_profile'),
    path('teacher/<int:teacher_id>/students/', views.teacher_students, name='teacher_students'),
    path('teacher/remove-student-mapping/<int:mapping_id>/', views.remove_student_mapping, name='remove_student_mapping'),  # Remove student-teacher mapping
    path('teacher/<int:teacher_id>/add-student/', views.add_student, name='add_student'),  # Updated URL pattern
    # Student URLs
    path('student/dashboard/<int:student_id>/', views.student_dashboard, name='student_dashboard'),
    path('student/update/<int:student_id>/', views.update_student, name='update_student'),
    # Admin/Utility URLs (for teachers to list students)

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
