"""
verification/urls.py
Main application URL patterns.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Dashboard (role-based)
    path('dashboard/', views.dashboard, name='dashboard'),

    # College Portal — Student Management
    path('college/students/', views.student_list, name='student_list'),
    path('college/students/add/', views.add_student, name='add_student'),
    path('college/students/<int:student_id>/', views.student_detail, name='student_detail'),

    # College Portal — Certificate Management
    path('college/certificates/', views.certificate_list, name='certificate_list'),
    path('college/certificates/upload/', views.upload_certificate, name='upload_certificate'),
    path('college/certificates/<int:cert_id>/', views.certificate_detail, name='certificate_detail'),

    # Company Portal — Verification
    path('company/verify/', views.verify_certificate, name='verify_certificate'),
    path('company/verify/result/<int:log_id>/', views.verification_result, name='verification_result'),
    path('company/history/', views.verification_history, name='verification_history'),

    # Blockchain Explorer
    path('blockchain/', views.blockchain_explorer, name='blockchain_explorer'),
]
