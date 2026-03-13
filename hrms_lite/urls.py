from django.contrib import admin
from django.urls import include, path

from .health import HealthCheckView, ReadinessCheckView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health checks
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('ready/', ReadinessCheckView.as_view(), name='readiness-check'),
    
    # API routes
    path('api/', include('hr.urls')),
    path('api/', include('attendance.urls')),
]
