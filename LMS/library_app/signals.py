from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BorrowedBook

@receiver(post_save, sender=BorrowedBook)
def book_borrowed_signal(sender, instance, created, **kwargs):
    """Print when a new book is borrowed"""
    if created:  
        print(f"  NEW BORROW: {instance.member.user.username} borrowed '{instance.book.title}'")
      