"""
verification/admin.py
Django admin configuration for certificate verification models.
"""

from django.contrib import admin
from .models import UserProfile, Student, Certificate, VerificationLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'institution_name', 'created_at']
    list_filter = ['role']
    search_fields = ['user__username', 'institution_name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'department', 'year_of_passing', 'college']
    list_filter = ['department', 'year_of_passing']
    search_fields = ['student_id', 'name', 'email']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'student', 'certificate_type',
        'transaction_id', 'block_index', 'created_at'
    ]
    list_filter = ['certificate_type', 'created_at']
    search_fields = ['title', 'student__name', 'transaction_id', 'file_hash']
    readonly_fields = ['file_hash', 'block_index', 'block_hash', 'transaction_id', 'ocr_text']


@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    list_display = [
        'uploaded_file_name', 'status', 'verified_by',
        'transaction_id', 'verified_at'
    ]
    list_filter = ['status', 'verified_at']
    search_fields = ['uploaded_file_name', 'uploaded_file_hash', 'transaction_id']
    readonly_fields = ['ocr_text']
