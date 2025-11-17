from django.db.models import Count, Sum, Q
# from ..models.django_orm import Member

from ..models.sqlalchemy_models import Member
from ..context.database import Session
from sqlalchemy import select, update

class MemberRepository:
    
    @staticmethod
    def get_all(filters=None):
        session = Session()
        stmt = select(Member)
        if filters:
            if filters.get('username'):
                stmt = stmt.where(Member.username.ilike(f"%{filters['username']}%"))
            if filters.get('phone_number'):
                stmt = stmt.where(Member.phone_number.ilike(f"%{filters['phone_number']}%"))
        
        return session.scalars(stmt).all()
    
    @staticmethod
    def get_by_id(member_id):
        session = Session()
        return session.get(Member, member_id)
    
    @staticmethod
    def get_by_username(username):
        session = Session()
        stmt = select(Member).where(Member.username == username)
        return session.scalar(stmt)
    
    @staticmethod
    def create(username, password, phone_number, is_staff=False):
        session = Session()
        member = Member(username=username, phone_number=phone_number, is_staff=is_staff)
        member.set_password(password)
        session.add(member)
        session.commit()
        session.refresh(member)
        return member
    
    @staticmethod
    def update_member(member, data):
        for key, value in data.items():
            setattr(member, key, value)
        session = Session()
        session.add(member)
        session.commit()
        session.refresh(member)  
        return member
        
    
    @staticmethod
    def delete_member(member):
        session = Session()
        session.delete(member)
        session.commit()
 
    