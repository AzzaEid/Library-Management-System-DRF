from django.db.models import Count, Sum, Q
from ..models import Member


class MemberRepository:
    
    @staticmethod
    def get_all_members():
        return Member.objects.select_related('user').all()
    
    @staticmethod
    def get_member_by_id(member_id):
        return Member.objects.select_related('user').get(id=member_id)
    
    @staticmethod
    def get_member_by_user(user):
        return Member.objects.get(user=user)
    
    @staticmethod
    def get_member_by_username(username):
        return Member.objects.select_related('user').get(user__username=username)
    
    @staticmethod
    def create_member(user, data):
        return Member.objects.create(user=user, **data)
    
    @staticmethod
    def update_member(member, data):
        for key, value in data.items():
            setattr(member, key, value)
        member.save()
        return member
    
    @staticmethod
    def delete_member(member):
        member.delete()
    
    