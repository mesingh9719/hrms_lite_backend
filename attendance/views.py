"""Attendance management views."""
import logging
from datetime import date

from django.db.models import Count, Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from hr.models import Employee
from .models import Attendance
from .serializers import AttendanceSerializer

logger = logging.getLogger(__name__)


class AttendanceListCreateView(generics.ListCreateAPIView):
    """List all attendance records or create a new one."""
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        queryset = Attendance.objects.select_related('employee').all()
        
        # Filter parameters
        employee_id = self.request.query_params.get('employee_id')
        date_param = self.request.query_params.get('date')
        status_param = self.request.query_params.get('status')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        if date_param:
            queryset = queryset.filter(date=date_param)
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating attendance record for employee: {request.data.get('employee')}")
        return super().create(request, *args, **kwargs)


class DashboardSummaryView(APIView):
    """Dashboard summary with attendance statistics."""
    
    def get(self, request):
        today = date.today()
        
        # Get overall statistics
        overall_stats = Attendance.objects.aggregate(
            total_records=Count('id'),
            total_present=Count('id', filter=Q(status='Present')),
            total_absent=Count('id', filter=Q(status='Absent')),
        )
        
        # Get today's statistics
        today_stats = Attendance.objects.filter(date=today).aggregate(
            present_today=Count('id', filter=Q(status='Present')),
            absent_today=Count('id', filter=Q(status='Absent')),
        )
        
        # Get employee count
        total_employees = Employee.objects.count()
        
        return Response({
            'total_employees': total_employees,
            'total_records': overall_stats['total_records'],
            'total_present': overall_stats['total_present'],
            'total_absent': overall_stats['total_absent'],
            'present_today': today_stats['present_today'],
            'absent_today': today_stats['absent_today'],
            'date': today.isoformat(),
        })
