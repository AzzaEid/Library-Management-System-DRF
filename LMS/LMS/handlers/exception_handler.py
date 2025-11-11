from rest_framework.views import exception_handler
import logging

logger = logging.getLogger('library_app')

def custom_exception_handler(exc, context):
    """
    Custom exception handler that formats error responses consistently.
    """
    response = exception_handler(exc, context)

    if response is not None:
        view = context.get('view')
        request = context.get('request')

        # Log the error
        logger.error(
            f"API Error in {view.__class__.__name__ if view else 'UnknownView'}: "
            f"{exc.__class__.__name__} - {str(exc)} "
            f"[{request.method if request else ''} {request.path if request else ''}]"
        )

        # Build the unified error structure
        error_data = {
            "success": False,
            "error": {
                "code": exc.__class__.__name__,
                "message": str(exc),
            }
        }

        # Add detailed errors (e.g., field validation issues)
        if hasattr(exc, "detail") and isinstance(exc.detail, dict):
            error_data["error"]["details"] = exc.detail

        response.data = error_data

    return response

