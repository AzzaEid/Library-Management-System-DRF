from django.utils import timezone
from django.db import models
from .book import Book
from .member import Member

class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_books')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrowed_books')
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    late_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    @property
    def is_returned(self):
        return self.returned_date is not None
    
    @property
    def is_overdue(self):
        if self.is_returned:
            return False
        return timezone.now().date() > self.due_date
    
    @property
    def days_overdue(self):
        if not self.is_overdue:
            return 0
        return (timezone.now().date() - self.due_date).days
    
    def __str__(self):
        return f"{self.book.title} borrowed by {self.member.user.username}"
