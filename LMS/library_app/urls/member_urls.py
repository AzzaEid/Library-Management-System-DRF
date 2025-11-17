from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.member_views import MemberBooksController

router = DefaultRouter()
router.register('books', MemberBooksController, basename='member-borrowed-book')
# router.register('profile', MemberProfileViewSet, basename="member-profile")

urlpatterns = [
    path('', include(router.urls)),
]