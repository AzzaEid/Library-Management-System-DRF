from library_app.models import Member
from ..repository import MemberRepository, BorrowedBookRepository
from django.contrib.auth.models import User

class MemberManagement:
    @staticmethod
    def get_all_members():
        return MemberRepository.get_all_members()
    
    @staticmethod
    def get_member_by_id(member_id):
        try:
            return MemberRepository.get_member_by_id(member_id)
        except Member.DoesNotExist:
            return None
        
    @staticmethod
    def create_member(username, password, phone_number):
        user = User.objects.create_user(username=username, password=password)
        member = MemberRepository.create_member(user, phone_number)
        return member
    
    @staticmethod
    def update_member(member_id, data):
        member = MemberManagement.get_member_by_id(member_id=member_id)
        if not member:
            return None
        
        return MemberRepository.update_member(member, data)
    
    @staticmethod
    def delete_member(member_id):
        member = MemberManagement.get_member_by_id(member_id=member_id)
        return MemberRepository.delete_member(member)
    
    @staticmethod
    def get_member_from_user(user):
        try:
            return user.member
        except (Member.DoesNotExist, AttributeError):
            return None
    
    @staticmethod
    def get_member_borrowed_books(member):
        borrowed_books = BorrowedBookRepository.get_borrowed_by_member(member)
        total_late_fees = sum(
            book.late_fee for book in borrowed_books if book.late_fee
        )
        return borrowed_books, total_late_fees
        
            