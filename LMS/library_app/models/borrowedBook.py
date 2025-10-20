from time import timezone
from django.db import models
from .book import Book
from .member import Member

class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_books')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrowed_books')
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    late_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_overdue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.member.user.username}"
