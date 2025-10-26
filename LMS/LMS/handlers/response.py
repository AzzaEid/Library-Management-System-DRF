
from rest_framework.renderers import JSONRenderer

class StandardJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response")
        success = response.status_code < 400
        
        formatted = {
            "success": success,
            "data": data if success else None,
        }

        if not success:
            formatted["error"] = data

        return super().render(formatted, accepted_media_type, renderer_context)
