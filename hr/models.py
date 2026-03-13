"""Employee models."""
from django.db import models


class Employee(models.Model):
    """Employee model representing a company employee."""
    
    employee_id = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        help_text='Unique employee identifier'
    )
    full_name = models.CharField(
        max_length=150,
        help_text='Full name of the employee'
    )
    email = models.EmailField(
        unique=True,
        db_index=True,
        help_text='Employee email address'
    )
    department = models.CharField(
        max_length=100,
        db_index=True,
        help_text='Department name'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['department', 'full_name']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"
