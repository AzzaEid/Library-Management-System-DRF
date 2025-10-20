from django.db.models import Count, Sum, Q
from ..models import Member


class MemberRepository:
    
   
    @staticmethod
    def get_member_by_username(username):
        return Member.objects.select_related('user').get(user__username=username)
    
    @staticmethod
    def create_member(user, data):
        return Member.objects.create(user=user, **data)
    
 
    