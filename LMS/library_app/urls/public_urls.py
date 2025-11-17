from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.public_views import PublicBookController, PublicAuthorController

router = DefaultRouter()
router.register('books', PublicBookController, basename='public-book')
router.register('authors', PublicAuthorController, basename='public-author')
# router.register('member-register', PublicMemberRegisterView, basename='public-register')


urlpatterns = [
    path('', include(router.urls)),
]