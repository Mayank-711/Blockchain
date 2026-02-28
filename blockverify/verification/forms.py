"""
verification/forms.py
Django forms for the Certificate Verification System.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Certificate, UserProfile


class RegistrationForm(UserCreationForm):
    """
    Registration form for college and company users.
    Extends Django's UserCreationForm with role and institution fields.
    """
    ROLE_CHOICES = (
        ('college', 'College'),
        ('company', 'Company'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    institution_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Institution / Company Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                institution_name=self.cleaned_data['institution_name']
            )
        return user


class LoginForm(forms.Form):
    """Login form for authentication."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class StudentForm(forms.ModelForm):
    """Form for adding / editing student details."""

    class Meta:
        model = Student
        fields = ['student_id', 'name', 'email', 'department', 'year_of_passing']
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Student ID (e.g., STU-2024-001)'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Department'
            }),
            'year_of_passing': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Year of Passing'
            }),
        }


class CertificateUploadForm(forms.ModelForm):
    """Form for uploading certificates (College Portal)."""

    class Meta:
        model = Certificate
        fields = [
            'student', 'title', 'certificate_type',
            'description', 'certificate_file', 'issued_date'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Certificate Title'
            }),
            'certificate_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description (optional)'
            }),
            'certificate_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.png,.jpg,.jpeg'
            }),
            'issued_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def __init__(self, *args, college_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if college_user:
            # Only show students belonging to this college
            self.fields['student'].queryset = Student.objects.filter(
                college=college_user
            )


class VerifyForm(forms.Form):
    """Form for company verification upload."""
    certificate_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.png,.jpg,.jpeg'
        }),
        help_text='Upload the certificate to verify (PDF or Image)'
    )
