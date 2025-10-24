from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.admin_views import (
    AdminBorrowedBookViewSet,
    AdminMemberViewSet,
    AdminBookViewSet,
    AdminAuthorViewSet
)
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register('borrowed-books', AdminBorrowedBookViewSet, basename='admin-borrowed-book')
router.register('members', AdminMemberViewSet, basename='admin-member')
router.register('books', AdminBookViewSet, basename='admin-book')
router.register('authors', AdminAuthorViewSet , basename='admin-author')

member_router = NestedDefaultRouter(router, r'members', lookup='member')
member_router.register(r'borrowed-books', AdminBorrowedBookViewSet, basename='admin-member-borrowed-books')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(member_router.urls))
]