from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger('library_app')


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error format.
    
    Format:
    {
        "success": false,
        "error": {
            "type": "ValidationError",
            "message": "Main error message",
            "details": {...}  # Optional field-specific errors
        }
    }
    """
    # Call DRF's default handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Standardize error response
        error_data = {
            'success': False,
            'error': {
                'type': exc.__class__.__name__,
                'message': str(exc),
            }
        }
        
        # Add field-specific details if available
        if hasattr(exc, 'detail'):
            error_data['error']['details'] = exc.detail
            
        # Log the error
        view = context.get('view')
        request = context.get('request')
        if view and request:
            logger.error(
                f"API Error in {view.__class__.__name__}: "
                f"{exc.__class__.__name__} - {str(exc)} "
                f"[{request.method} {request.path}]"
            )
        
        response.data = error_data
    
    return response
