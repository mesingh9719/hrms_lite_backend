"""
Custom exception handling for HRMS Lite.
"""
import logging

from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


class ServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Service temporarily unavailable. Please try again later.'
    default_code = 'service_unavailable'


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request.'
    default_code = 'bad_request'


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses.
    """
    # Log the exception
    logger.error(
        f"Exception occurred: {type(exc).__name__} - {str(exc)}",
        exc_info=True,
        extra={
            'view': context.get('view'),
            'request': context.get('request'),
        }
    )

    # Handle Django ValidationError
    if isinstance(exc, DjangoValidationError):
        exc = ValidationError(detail=exc.messages)

    # Handle 404 errors
    if isinstance(exc, Http404):
        return Response(
            {
                'success': False,
                'error': {
                    'code': 'not_found',
                    'message': 'Resource not found.',
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # Get the standard error response
    response = exception_handler(exc, context)

    if response is not None:
        # Format the error response
        error_response = {
            'success': False,
            'error': {
                'code': getattr(exc, 'default_code', 'error'),
                'message': _get_error_message(response.data),
            }
        }
        
        # Include field errors for validation errors
        if isinstance(exc, ValidationError) and isinstance(response.data, dict):
            field_errors = {}
            for field, errors in response.data.items():
                if isinstance(errors, list):
                    field_errors[field] = errors[0] if len(errors) == 1 else errors
                else:
                    field_errors[field] = errors
            error_response['error']['fields'] = field_errors
        
        response.data = error_response

    return response


def _get_error_message(data):
    """Extract a human-readable error message from response data."""
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        return data[0] if data else 'An error occurred.'
    if isinstance(data, dict):
        if 'detail' in data:
            return data['detail']
        if 'non_field_errors' in data:
            errors = data['non_field_errors']
            return errors[0] if isinstance(errors, list) else errors
        # Get first field error
        for field, errors in data.items():
            if isinstance(errors, list):
                return f"{field}: {errors[0]}"
            return f"{field}: {errors}"
    return 'An error occurred.'
