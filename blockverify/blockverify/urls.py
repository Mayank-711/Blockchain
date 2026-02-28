"""
blockverify/urls.py
Root URL configuration for BlockVerify project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('auth/', include('verification.urls_auth')),

    # Main application URLs
    path('', include('verification.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
