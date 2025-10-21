from django.core.management.base import BaseCommand
from django.utils import timezone
from library_app.models import BorrowedBook
from django.db import transaction

class Command(BaseCommand):
    help = 'Set all borrowed books as returned'
    
    def handle(self, *args, **kwargs):
        borrowed_books = BorrowedBook.objects.filter(returned_date__isnull=True)
        count = borrowed_books.count()
        
        if count == 0:
            self.stdout.write(self.style.WARNING('No borrowed books to return'))
            return
        
        now = timezone.now().date()
        
        with transaction.atomic():
            borrowed_books.update(returned_date=now)

        self.stdout.write(self.style.SUCCESS(f'Successfully returned {count} books'))
