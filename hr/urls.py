from django.urls import path

from .views import EmployeeAttendanceView, EmployeeRetrieveUpdateDeleteView, EmployeeListCreateView

urlpatterns = [
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDeleteView.as_view(), name='employee-detail'),
    path(
        'employees/<int:pk>/attendance/',
        EmployeeAttendanceView.as_view(),
        name='employee-attendance',
    ),
]
