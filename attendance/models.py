"""Attendance models."""
from django.db import models

from hr.models import Employee


class Attendance(models.Model):
    """Attendance model for tracking employee attendance."""
    
    class Status(models.TextChoices):
        PRESENT = 'Present', 'Present'
        ABSENT = 'Absent', 'Absent'

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendances',
        help_text='Employee being tracked'
    )
    date = models.DateField(
        db_index=True,
        help_text='Attendance date'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        db_index=True,
        help_text='Attendance status'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'date'],
                name='unique_employee_date'
            ),
        ]
        indexes = [
            models.Index(fields=['date', 'status']),
            models.Index(fields=['employee', 'date']),
        ]

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"
