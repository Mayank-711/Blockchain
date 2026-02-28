"""
verification/views.py
Views for the Blockchain-Based Certificate Verification System.

Sections:
    - Home & Dashboard
    - College Portal (add students, upload certificates)
    - Company Portal (verify certificates)
    - Blockchain Explorer
"""

import os
import uuid
import logging
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .models import Student, Certificate, VerificationLog
from .forms import (
    RegistrationForm, LoginForm, StudentForm,
    CertificateUploadForm, VerifyForm
)
from .decorators import role_required
from blockchain import Blockchain
from services import OCRService, HashService

logger = logging.getLogger(__name__)

# Initialize blockchain singleton
blockchain = Blockchain()


# ============================================
# HOME & DASHBOARD
# ============================================

def home(request):
    """Landing page for the application."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')


@login_required
def dashboard(request):
    """
    Unified dashboard that redirects to role-specific dashboard.
    """
    if not hasattr(request.user, 'profile'):
        messages.error(request, 'User profile not configured. Contact admin.')
        return redirect('home')

    role = request.user.profile.role

    if role == 'college':
        return _college_dashboard(request)
    elif role == 'company':
        return _company_dashboard(request)
    else:
        messages.error(request, 'Unknown user role.')
        return redirect('home')


def _college_dashboard(request):
    """College dashboard with stats and recent activity."""
    students = Student.objects.filter(college=request.user)
    certificates = Certificate.objects.filter(uploaded_by=request.user)

    context = {
        'total_students': students.count(),
        'total_certificates': certificates.count(),
        'recent_students': students[:5],
        'recent_certificates': certificates[:5],
        'blockchain_length': blockchain.get_chain_length(),
        'chain_valid': blockchain.is_chain_valid(),
    }
    return render(request, 'college/dashboard.html', context)


def _company_dashboard(request):
    """Company dashboard with verification stats."""
    logs = VerificationLog.objects.filter(verified_by=request.user)

    context = {
        'total_verifications': logs.count(),
        'verified_count': logs.filter(status='verified').count(),
        'tampered_count': logs.filter(status='tampered').count(),
        'not_found_count': logs.filter(status='not_found').count(),
        'recent_verifications': logs[:10],
    }
    return render(request, 'company/dashboard.html', context)


# ============================================
# COLLEGE PORTAL — STUDENT MANAGEMENT
# ============================================

@login_required
@role_required('college')
def add_student(request):
    """Add a new student to the college."""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.college = request.user
            student.save()
            messages.success(
                request,
                f'Student "{student.name}" added successfully!'
            )
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'college/add_student.html', {'form': form})


@login_required
@role_required('college')
def student_list(request):
    """List all students added by this college."""
    students = Student.objects.filter(college=request.user)
    return render(request, 'college/student_list.html', {'students': students})


@login_required
@role_required('college')
def student_detail(request, student_id):
    """View student details and their certificates."""
    student = get_object_or_404(
        Student, id=student_id, college=request.user
    )
    certificates = Certificate.objects.filter(student=student)
    return render(request, 'college/student_detail.html', {
        'student': student,
        'certificates': certificates,
    })


# ============================================
# COLLEGE PORTAL — CERTIFICATE UPLOAD
# ============================================

@login_required
@role_required('college')
def upload_certificate(request):
    """
    Upload a certificate for a student.
    Process:
        1. Save uploaded file to media folder.
        2. Run OCR using Gemma AI service.
        3. Generate SHA-256 hash of the file.
        4. Store hash + metadata in blockchain.
        5. Save blockchain transaction ID in database.
    """
    if request.method == 'POST':
        form = CertificateUploadForm(
            request.POST, request.FILES, college_user=request.user
        )
        if form.is_valid():
            try:
                certificate = form.save(commit=False)
                certificate.uploaded_by = request.user
                certificate.transaction_id = str(uuid.uuid4())

                # Step 1: Save file first to get the path
                certificate.save()
                file_path = certificate.certificate_file.path

                # Step 2: OCR text extraction using Gemma AI
                logger.info(f"Running OCR on: {file_path}")
                ocr_text = OCRService.extract_text(file_path)
                certificate.ocr_text = ocr_text

                # Step 3: Generate SHA-256 hash of the file
                file_hash = HashService.hash_file(file_path)
                certificate.file_hash = file_hash

                # Step 4: Add to blockchain
                block_data = {
                    'certificate_hash': file_hash,
                    'student_name': certificate.student.name,
                    'student_id': certificate.student.student_id,
                    'certificate_type': certificate.certificate_type,
                    'title': certificate.title,
                    'transaction_id': certificate.transaction_id,
                    'institution': request.user.profile.institution_name,
                    'timestamp': datetime.now().isoformat(),
                }
                new_block = blockchain.add_block(block_data)

                # Step 5: Save blockchain metadata
                certificate.block_index = new_block.index
                certificate.block_hash = new_block.current_hash
                certificate.save()

                logger.info(
                    f"Certificate uploaded: {certificate.title} | "
                    f"Block #{new_block.index} | Hash: {file_hash[:16]}..."
                )

                messages.success(
                    request,
                    f'Certificate "{certificate.title}" uploaded and stored '
                    f'on blockchain (Block #{new_block.index})!'
                )
                return redirect('certificate_detail', cert_id=certificate.id)

            except Exception as e:
                logger.error(f"Certificate upload failed: {e}")
                messages.error(request, f'Upload failed: {e}')
    else:
        form = CertificateUploadForm(college_user=request.user)

    return render(request, 'college/upload_certificate.html', {'form': form})


@login_required
@role_required('college')
def certificate_list(request):
    """List all certificates uploaded by this college."""
    certificates = Certificate.objects.filter(uploaded_by=request.user)
    return render(request, 'college/certificate_list.html', {
        'certificates': certificates
    })


@login_required
@role_required('college')
def certificate_detail(request, cert_id):
    """View detailed certificate info including blockchain data."""
    certificate = get_object_or_404(
        Certificate, id=cert_id, uploaded_by=request.user
    )

    # Get block from blockchain
    block = blockchain.get_block(certificate.block_index) if certificate.block_index else None

    return render(request, 'college/certificate_detail.html', {
        'certificate': certificate,
        'block': block.to_dict() if block else None,
    })


# ============================================
# COMPANY PORTAL — VERIFICATION
# ============================================

@login_required
@role_required('company')
def verify_certificate(request):
    """
    Company uploads a certificate for verification.
    Process:
        1. Run OCR on uploaded file.
        2. Generate SHA-256 hash.
        3. Search blockchain for matching hash.
        4. Return verification result.
    """
    if request.method == 'POST':
        form = VerifyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded_file = request.FILES['certificate_file']

                # Save temporarily to run OCR
                temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
                os.makedirs(temp_dir, exist_ok=True)
                temp_path = os.path.join(temp_dir, uploaded_file.name)

                with open(temp_path, 'wb+') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)

                # Step 1: OCR text extraction
                ocr_text = OCRService.extract_text(temp_path)

                # Step 2: Generate SHA-256 hash
                file_hash = HashService.hash_file(temp_path)

                # Step 3: Search blockchain
                block = blockchain.find_by_hash(file_hash)

                # Step 4: Determine verification status
                if block:
                    status = 'verified'
                    # Find the matching certificate in the database
                    matched_cert = Certificate.objects.filter(
                        file_hash=file_hash
                    ).first()
                else:
                    status = 'tampered'
                    matched_cert = None

                # Log the verification
                log = VerificationLog.objects.create(
                    verified_by=request.user,
                    uploaded_file_name=uploaded_file.name,
                    uploaded_file_hash=file_hash,
                    status=status,
                    matched_certificate=matched_cert,
                    block_index=block.index if block else None,
                    block_hash=block.current_hash if block else '',
                    transaction_id=block.data.get('transaction_id', '') if block else '',
                    ocr_text=ocr_text,
                )

                # Clean up temp file
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

                return redirect('verification_result', log_id=log.id)

            except Exception as e:
                logger.error(f"Verification failed: {e}")
                messages.error(request, f'Verification failed: {e}')
    else:
        form = VerifyForm()

    return render(request, 'company/verify.html', {'form': form})


@login_required
@role_required('company')
def verification_result(request, log_id):
    """Display verification result details."""
    log = get_object_or_404(
        VerificationLog, id=log_id, verified_by=request.user
    )

    # Get block details if available
    block = None
    if log.block_index is not None:
        block_obj = blockchain.get_block(log.block_index)
        if block_obj:
            block = block_obj.to_dict()

    return render(request, 'company/verification_result.html', {
        'log': log,
        'block': block,
    })


@login_required
@role_required('company')
def verification_history(request):
    """Show all past verification attempts."""
    logs = VerificationLog.objects.filter(verified_by=request.user)
    return render(request, 'company/verification_history.html', {
        'logs': logs
    })


# ============================================
# BLOCKCHAIN EXPLORER
# ============================================

@login_required
def blockchain_explorer(request):
    """View the full blockchain (available to all logged-in users)."""
    blocks = blockchain.get_all_blocks()
    chain_valid = blockchain.is_chain_valid()

    return render(request, 'blockchain_explorer.html', {
        'blocks': blocks,
        'chain_valid': chain_valid,
        'chain_length': blockchain.get_chain_length(),
    })
