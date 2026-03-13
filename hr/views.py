"""Employee management views."""
import logging

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from attendance.serializers import AttendanceSerializer
from .models import Employee
from .serializers import EmployeeSerializer

logger = logging.getLogger(__name__)


class EmployeeListCreateView(generics.ListCreateAPIView):
    """List all employees or create a new employee."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        """Optionally filter employees by department."""
        queryset = super().get_queryset()
        department = self.request.query_params.get('department')
        search = self.request.query_params.get('search')
        
        if department:
            queryset = queryset.filter(department__iexact=department)
        if search:
            queryset = queryset.filter(
                full_name__icontains=search
            ) | queryset.filter(
                employee_id__icontains=search
            ) | queryset.filter(
                email__icontains=search
            )
        return queryset

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating employee: {request.data.get('employee_id')}")
        return super().create(request, *args, **kwargs)


class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an employee."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def destroy(self, request, *args, **kwargs):
        employee = self.get_object()
        employee_name = employee.full_name
        logger.info(f"Deleting employee: {employee.employee_id} - {employee_name}")
        self.perform_destroy(employee)
        return Response(
            {
                'success': True,
                'message': f'Employee {employee_name} deleted successfully.',
            },
            status=status.HTTP_200_OK,
        )


class EmployeeAttendanceView(generics.ListAPIView):
    """List attendance records for a specific employee."""
    serializer_class = AttendanceSerializer

    def get_employee(self):
        return get_object_or_404(Employee, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_employee().attendances.select_related('employee').all()
