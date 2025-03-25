from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
import logging

# Configure logger
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for more detailed error responses
    """
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, ValueError):
            response = Response({
                'error': 'Invalid value',
                'detail': str(exc)
            }, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, PermissionError):
            response = Response({
                'error': 'Permission denied',
                'detail': str(exc)
            }, status=status.HTTP_403_FORBIDDEN)
        else:
            logger.error(f"Unhandled exception: {exc}", exc_info=True)
            response = Response({
                'error': 'Internal server error',
                'detail': 'An unexpected error occurred'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if response is not None:
        logger.error(
            f"Error Response: {response.status_code} - {response.data}",
            extra={
                'status_code': response.status_code,
                'error_detail': response.data
            }
        )
    
    return response

class TaskAssignmentError(Exception):
    """
    Custom exception for task assignment errors
    """
    def __init__(self, message="Task assignment failed"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundException(Exception):
    """
    Custom exception for user not found scenarios
    """
    def __init__(self, user_id):
        self.message = f"User with ID {user_id} not found"
        super().__init__(self.message)