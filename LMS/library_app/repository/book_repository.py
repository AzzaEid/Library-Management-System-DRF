from django.db.models import Q, Count
from ..models.sqlalchemy_models import Book, MemberBook
from django.db.models import F
from sqlalchemy import func, select, update
from sqlalchemy.orm import joinedload
from ..context.database import Session


class BookRepository:
    @staticmethod
    def get_all():
        session = Session()
        stmt = select(Book).options(joinedload(Book.author))
        return session.scalars(stmt).unique().all()
    
    @staticmethod
    def get_by_id(book_id):
        session = Session()
        stmt = select(Book).options(joinedload(Book.author)).where(Book.id == book_id)
        return session.scalar(stmt)
    
    @staticmethod
    def get_for_update(book_id):
        session = Session()
        stmt = select(Book).with_for_update().options(joinedload(Book.author)).where(Book.id == book_id)
        return session.scalar(stmt)
    
    @staticmethod
    def create(data):
        session = Session()
        book = Book(**data)
        session.add(book)
        session.commit()
        session.refresh(book)
        return book
    
    @staticmethod
    def update(book, data):
        session = Session()
        for key, value in data.items():
            setattr(book, key, value)
        session.add(book)
        session.commit()
        session.refresh(book)
        return book
    
    @staticmethod
    def delete(book):
        session = Session()
        session.delete(book)
        session.commit()
    
    @staticmethod
    def get_borrowed_copies(book_id):
        session = Session()
        count = session.query(func.count(MemberBook.id)).filter(
            MemberBook.book_id == book_id,
            MemberBook.returned_date.is_(None)
        ).scalar()
        return count or 0
    
    @staticmethod
    def is_available(book_id):
        session = Session()
        book = session.get(Book, book_id)
        if not book:
            return False
        borrowed = BookRepository.get_borrowed_copies(book_id)
        return book.total_copies > borrowed
