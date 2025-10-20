from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
   openapi.Info(
      title="Library API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(AllowAny,),
)
