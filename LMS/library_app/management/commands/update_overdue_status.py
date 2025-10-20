from django.core.management.base import BaseCommand
from django.utils import timezone
from library_app.models import BorrowedBook


class Command(BaseCommand):
    help = 'Update is_overdue status for all borrowed books'
    
    def handle(self, *args, **kwargs):
        borrowed_books = BorrowedBook.objects.all()

        today = timezone.now().date()
        overdue_count = 0
        
        for bb in borrowed_books:
            if bb.is_returned:
                continue
            if today > bb.due_date:
                bb.is_overdue = True
                bb.save()
                overdue_count += 1
                days = (today - bb.due_date).days
                self.stdout.write(f'  - Overdue: {bb.book.title} (Member: {bb.member.user.username}, {days} days late)')
           
        self.stdout.write(self.style.SUCCESS(f'\nFound {overdue_count} overdue'))


