from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.public_views import PublicBookViewSet, PublicAuthorViewSet, PublicMemberRegisterView

router = DefaultRouter()
router.register('books', PublicBookViewSet, basename='public-book')
router.register('authors', PublicAuthorViewSet, basename='public-author')
router.register('member-register', PublicMemberRegisterView, basename='public-register')


urlpatterns = [
    path('', include(router.urls)),
]