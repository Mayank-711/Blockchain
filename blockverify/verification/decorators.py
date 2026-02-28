"""
verification/decorators.py
Custom decorators for role-based access control.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(role):
    """
    Decorator to restrict view access to a specific user role.

    Usage:
        @role_required('college')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Please log in to access this page.')
                return redirect('login')

            if not hasattr(request.user, 'profile'):
                messages.error(request, 'User profile not found.')
                return redirect('login')

            if request.user.profile.role != role:
                messages.error(
                    request,
                    f'Access denied. This page is for {role} users only.'
                )
                return redirect('dashboard')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
