from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.member_views import MemberBorrowedBookViewSet, MemberProfileViewSet

router = DefaultRouter()
router.register('borrowed-books', MemberBorrowedBookViewSet, basename='member-borrowed-book')
router.register('profile', MemberProfileViewSet, basename="member-profile")

urlpatterns = [
    path('', include(router.urls)),
]