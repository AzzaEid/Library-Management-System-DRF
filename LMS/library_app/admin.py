from django.contrib import admin
from .models import Author, Book, Member, BorrowedBook

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'isbn', 'total_copies', 'borrowed_copies']
    list_filter = ['author']
    search_fields = ['title', 'isbn']
    readonly_fields = ['borrowed_copies']  

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_username', 'phone_number', 'joined_date']
    search_fields = ['user__username', 'phone_number']
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'member', 'borrowed_date', 'due_date', 
                    'get_is_returned', 'get_is_overdue', 'late_fee'] 
    search_fields = ['book__title', 'member__user__username']
    list_filter = ['borrowed_date', 'due_date', 'returned_date']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['borrowed_date', 'late_fee']
        return []
    
    def get_fields(self, request, obj=None):
        if obj:
            return ['book', 'member', 'borrowed_date', 'due_date', 'returned_date', 'late_fee']
        else:
            return ['book', 'member', 'due_date']
    
    def get_is_returned(self, obj):
        return obj.is_returned
    get_is_returned.boolean = True
    get_is_returned.short_description = 'Returned'
    
    def get_is_overdue(self, obj):
        return obj.is_overdue
    get_is_overdue.boolean = True
    get_is_overdue.short_description = 'Overdue'