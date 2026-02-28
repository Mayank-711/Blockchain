"""
verification/apps.py
App configuration for the verification module.
"""

from django.apps import AppConfig


class VerificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'verification'
    verbose_name = 'Certificate Verification'
