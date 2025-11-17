from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.admin_views import (
    AdminBorrowedBooksController,
    AdminMembersController,
    AdminBooksController,
    AdminAuthorsController,
)
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register('member-books', AdminBorrowedBooksController, basename='admin-member-book') 
router.register('members', AdminMembersController, basename='admin-member')
router.register('books', AdminBooksController, basename='admin-book')
router.register('authors', AdminAuthorsController, basename='admin-author')

# Nested router for member -> borrowed-books
member_router = NestedDefaultRouter(router, r'members', lookup='member')
member_router.register(r'borrowed-books', AdminBorrowedBooksController, basename='member-borrowed-books')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(member_router.urls)),
]