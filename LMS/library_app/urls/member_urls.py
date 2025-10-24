from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.member_views import MemberBorrowedBookViewSet

router = DefaultRouter()
router.register('borrowed-books', MemberBorrowedBookViewSet, basename='member-borrowed-book')

urlpatterns = [
    path('', include(router.urls)),
]