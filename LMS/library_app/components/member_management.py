# from LMS.library_app.models.django_orm import Member
from ..repository import MemberRepository, BorrowedBookRepository
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
class MemberManagement:
    def __init__(self, **kwargs):
        self.member_repo = MemberRepository()
        super().__init__(**kwargs)
        
    def get_all_members(self, filters=None):
        return self.member_repo.get_all(filters=None)
    
    def get_member_by_id(self, member_id):
        try:
            return self.member_repo.get_by_id(member_id)
        except :
            raise ValidationError({'member':"Doesn't exist"})
    

    def create_member(self, username, password, phone_number, is_staff=False):
        return self.member_repo.create(username, password, phone_number, is_staff)
    
    def update_member(self, member_id, data):
        member = self.get_member_by_id(member_id=member_id)
        if not member:
            return None
        
        return self.member_repo.update_member(member, data)
    
    def delete_member(self, member_id):
        member = self.get_member_by_id(member_id=member_id)
        return self.member_repo.delete_member(member)
    
    def get_member_from_user(self, user):
        try:
            return user.member
        except :
            raise ValidationError({'member':"Doesn't exist"})
        
    def get_member_borrowed_books(self, member_id):
        borrowed_books = BorrowedBookRepository.get_borrowed_by_member(member_id)
        total_late_fees = sum(
            book.late_fee for book in borrowed_books if book.late_fee
        )
        return borrowed_books, total_late_fees
        
            