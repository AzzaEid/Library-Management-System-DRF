from django.urls import include, path
from rest_framework.routers import DefaultRouter
from library_app.views import AuthorViewSet, BookViewSet, MemberViewSet, BorrowedBookViewSet, ReturnBookView
from rest_framework_nested.routers import NestedDefaultRouter


router =  DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'members', MemberViewSet)
router.register(r'borrowed-books', BorrowedBookViewSet)
 
members_router = NestedDefaultRouter(router, r'members', lookup='member')
members_router.register(r'borrowed-books', BorrowedBookViewSet, basename='member-borrowed-books')


urlpatterns = [path('', include(router.urls)),
               path('return-books/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
               path('', include(members_router.urls)),

               ]