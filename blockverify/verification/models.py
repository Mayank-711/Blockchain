"""
verification/models.py
Database models for the Certificate Verification System.

Models:
    - UserProfile: Extends User with role (college/company).
    - Student: Student information added by colleges.
    - Certificate: Uploaded certificates with blockchain metadata.
    - VerificationLog: Log of company verification attempts.
"""

from django.db import models
from django.contrib.auth.models import User
import uuid


class UserProfile(models.Model):
    """
    Extended user profile with role-based access.
    Each user is either a 'college' or 'company'.
    """
    ROLE_CHOICES = (
        ('college', 'College'),
        ('company', 'Company'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    institution_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.institution_name} ({self.role})"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class Student(models.Model):
    """
    Student information added by a college portal.
    """
    student_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    department = models.CharField(max_length=255, blank=True)
    year_of_passing = models.IntegerField(null=True, blank=True)
    college = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='students'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Certificate(models.Model):
    """
    Certificate uploaded by college with blockchain metadata.
    """
    CERT_TYPE_CHOICES = (
        ('academic', 'Academic Certificate'),
        ('internship', 'Internship Certificate'),
        ('achievement', 'Achievement Certificate'),
        ('course', 'Course Completion'),
        ('other', 'Other'),
    )

    # Unique transaction ID for this certificate
    transaction_id = models.CharField(
        max_length=64, unique=True, default=uuid.uuid4
    )

    # Relationships
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='certificates'
    )
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='uploaded_certificates'
    )

    # Certificate details
    title = models.CharField(max_length=255)
    certificate_type = models.CharField(
        max_length=20, choices=CERT_TYPE_CHOICES, default='academic'
    )
    description = models.TextField(blank=True)

    # File
    certificate_file = models.FileField(upload_to='certificates/%Y/%m/')

    # Blockchain data
    file_hash = models.CharField(max_length=64)
    block_index = models.IntegerField(null=True, blank=True)
    block_hash = models.CharField(max_length=64, blank=True)

    # OCR extracted text
    ocr_text = models.TextField(blank=True)

    # Timestamps
    issued_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.student.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'


class VerificationLog(models.Model):
    """
    Log of every verification attempt by companies.
    """
    STATUS_CHOICES = (
        ('verified', 'Verified'),
        ('tampered', 'Tampered / Invalid'),
        ('not_found', 'Not Found'),
    )

    # Who verified
    verified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='verifications'
    )

    # Uploaded file details
    uploaded_file_name = models.CharField(max_length=255)
    uploaded_file_hash = models.CharField(max_length=64)

    # Result
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    matched_certificate = models.ForeignKey(
        Certificate, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='verification_logs'
    )

    # Blockchain details (if matched)
    block_index = models.IntegerField(null=True, blank=True)
    block_hash = models.CharField(max_length=64, blank=True)
    transaction_id = models.CharField(max_length=64, blank=True)

    # OCR text from uploaded file
    ocr_text = models.TextField(blank=True)

    # Timestamps
    verified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uploaded_file_name} - {self.status}"

    class Meta:
        ordering = ['-verified_at']
        verbose_name = 'Verification Log'
        verbose_name_plural = 'Verification Logs'
