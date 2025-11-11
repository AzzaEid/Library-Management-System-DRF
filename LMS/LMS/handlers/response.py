
from rest_framework.renderers import JSONRenderer

class StandardJSONRenderer(JSONRenderer):
    """
    Wrap all successful responses in a consistent structure.
    Error responses are already formatted by the custom exception handler.
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None
        status_code = response.status_code if response else 200

        # Only wrap successful responses
        if response and status_code < 400:
            formatted = {
                "success": True,
                "data": data,
                "message": "Operation completed successfully"
            }
        else:
            # Keep the error format as-is (already formatted by exception handler)
            formatted = data

        return super().render(formatted, accepted_media_type, renderer_context)