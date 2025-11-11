from django.db import models
from .author import Author

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=20, unique=True)
    total_copies = models.PositiveIntegerField(default=1)
    borrowed_copies = models.PositiveIntegerField(default=0)
    
    # @property
    # def borrowed_copies(self): <<< N+1 PROBLEM
    #     return self.borrowed_books.filter(is_returned=False).count()
    
    @property
    def available_copies(self):
        return self.total_copies - self.borrowed_copies

    def __str__(self):
        return self.title

   