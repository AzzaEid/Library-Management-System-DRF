from django.db.models import Count, Sum, Q
# from ..models.django_orm import Member

from ..models.sqlalchemy_models import Member
from ..context.database import Session
from sqlalchemy import select, update

class MemberRepository:
    
    @staticmethod
    def get_all():
        session = Session()
        stmt = select(Member)
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
    def create(data):
        session = Session()
        member = Member(**data)
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
 
    