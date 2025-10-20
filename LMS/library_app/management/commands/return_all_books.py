from django.core.management.base import BaseCommand
from django.utils import timezone
from library_app.models import BorrowedBook


class Command(BaseCommand):
    help = 'Set all borrowed books as returned'
    
    def handle(self, *args, **kwargs):
        borrowed_books_row = BorrowedBook.objects.all()

        now = timezone.now().date()
        counter = 0
        for bb in borrowed_books_row:
            if bb.is_returned:
                continue 
            bb.is_returned = True
            bb.returned_date = now
            counter += 1
            bb.save()
            
            bb.book.borrowed_copies -= 1
            bb.book.save()
            self.stdout.write(f'  - Returned: {bb.book.title} Member: {bb.member.user.username}  ')

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully returned {counter} books'))
