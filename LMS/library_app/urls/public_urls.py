from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.public_views import PublicBookViewSet, PublicAuthorViewSet

router = DefaultRouter()
router.register('books', PublicBookViewSet, basename='public-book')
router.register('authors', PublicAuthorViewSet, basename='public-author')



urlpatterns = [
    path('', include(router.urls)),
]