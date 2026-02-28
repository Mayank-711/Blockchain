"""
verification/urls_auth.py
Authentication URL patterns (login, logout, register).
"""

from django.urls import path
from . import views_auth

urlpatterns = [
    path('login/', views_auth.login_view, name='login'),
    path('logout/', views_auth.logout_view, name='logout'),
    path('register/', views_auth.register_view, name='register'),
]
