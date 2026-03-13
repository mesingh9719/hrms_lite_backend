"""
Health check views for monitoring.
"""
import logging
from datetime import datetime

from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    """
    Basic health check endpoint.
    Returns 200 OK if the service is running.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'hrms-lite-api',
        })


class ReadinessCheckView(APIView):
    """
    Readiness check endpoint.
    Verifies database connectivity and other dependencies.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        checks = {
            'database': self._check_database(),
        }
        
        all_healthy = all(check['status'] == 'healthy' for check in checks.values())
        
        return Response(
            {
                'status': 'ready' if all_healthy else 'not_ready',
                'timestamp': datetime.utcnow().isoformat(),
                'checks': checks,
            },
            status=status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        )

    def _check_database(self):
        """Check database connectivity."""
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            return {'status': 'healthy', 'message': 'Database connection successful'}
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {'status': 'unhealthy', 'message': str(e)}
