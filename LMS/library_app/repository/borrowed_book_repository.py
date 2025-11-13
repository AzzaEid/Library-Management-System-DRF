from django.conf import settings
from django.db.models import Q, F
from django.utils import timezone
from datetime import date, timedelta
from ..models.sqlalchemy_models import Book, MemberBook
from django.db.models import F
from ..context.database import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from django.conf import settings

class MemberBookRepository:
    @staticmethod
    def get_all_borrowed():
        session = Session()
        stmt = select(MemberBook).options(
            joinedload(MemberBook.book),
            joinedload(MemberBook.member)
        )
        return session.scalars(stmt).all()
    
    @staticmethod
    def get_by_id(borrowed_id):
        session = Session()
        stmt = select(MemberBook).options(
            joinedload(MemberBook.book).joinedload(Book.author),
            joinedload(MemberBook.member)
        ).where(MemberBook.id == borrowed_id)
        return session.scalars(stmt)
    
    
    @staticmethod
    def create_borrow(book_id, member_id, period_days):
        session = Session()
        member_book = MemberBook(
            book_id=book_id,
            member_id=member_id,
            due_date=timezone.now().date() + timedelta(days=period_days),
            borrowed_date=timezone.now().date()
        )
        session.add(member_book)
        session.commit()
        session.refresh(member_book)
        return member_book
    

    @staticmethod
    def return_book(member_book_id):
        session = Session()
        member_book = session.get(MemberBook, member_book_id)
        if member_book:
            return_date = date.today()
            member_book.returned_date = return_date
            
            if return_date > member_book.due_date:
                days_late = (return_date - member_book.due_date).days
                member_book.late_fee = days_late * settings.LATE_FEE_PER_DAY
            
            session.commit()
            session.refresh(member_book)
        return member_book
    
    @staticmethod
    def get_overdue():
        session = Session()
        today = date.today()
        stmt = select(MemberBook).options(
            joinedload(MemberBook.book),
            joinedload(MemberBook.member)
        ).where(
            MemberBook.returned_date.is_(None),
            MemberBook.due_date < today
        )

        return session.scalars(stmt).all()
    
    @staticmethod
    def get_not_returned():
        session = Session()
        today = date.today()
        stmt = select(MemberBook).options(
            joinedload(MemberBook.book),
            joinedload(MemberBook.member)
        ).where(MemberBook.returned_date.is_(None))
        return session.scalars(stmt).all()
    
    
    @staticmethod
    def get_borrowed_by_member(member_id):
        session = Session()
        today = date.today()
        stmt = select(MemberBook).options(
            joinedload(MemberBook.book),
            joinedload(MemberBook.member)
        ).where(MemberBook.member_id == member_id)
        return session.scalars(stmt).all()