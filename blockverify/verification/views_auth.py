"""
verification/views_auth.py
Authentication views: login, logout, registration.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegistrationForm


def login_view(request):
    """Handle user login with role-based redirect."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def register_view(request):
    """Handle user registration with role selection."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            role = form.cleaned_data['role']
            messages.success(
                request,
                f'Account created successfully! Welcome to '
                f'BlockVerify as a {role}.'
            )
            return redirect('dashboard')
    else:
        form = RegistrationForm()

    return render(request, 'auth/register.html', {'form': form})
