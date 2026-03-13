"""
Base view classes for HRMS Lite.
Provides common functionality for all views.
"""
import logging

from rest_framework import generics, status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class BaseListCreateAPIView(generics.ListCreateAPIView):
    """
    Base view for list and create operations with logging.
    """
    
    def list(self, request, *args, **kwargs):
        logger.debug(f"Listing {self.get_queryset().model.__name__} objects")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Creating {self.get_queryset().model.__name__} object")
        return super().create(request, *args, **kwargs)


class BaseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Base view for retrieve, update, and destroy operations with logging.
    """
    
    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving {self.get_queryset().model.__name__} object: {kwargs}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Updating {self.get_queryset().model.__name__} object: {kwargs}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Deleting {self.get_queryset().model.__name__} object: {kwargs}")
        return super().destroy(request, *args, **kwargs)


class SuccessResponseMixin:
    """
    Mixin to provide consistent success responses.
    """
    
    def get_success_response(self, data=None, message=None, status_code=status.HTTP_200_OK):
        response_data = {'success': True}
        if message:
            response_data['message'] = message
        if data is not None:
            response_data['data'] = data
        return Response(response_data, status=status_code)

    def get_created_response(self, data, message=None):
        return self.get_success_response(
            data=data,
            message=message or 'Created successfully.',
            status_code=status.HTTP_201_CREATED
        )

    def get_deleted_response(self, message=None):
        return self.get_success_response(
            message=message or 'Deleted successfully.',
            status_code=status.HTTP_200_OK
        )
