from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import DECIMAL, Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import  DeclarativeBase, relationship, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    

class Author(Base):
    __tablename__ = 'authors'
    
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    bio: Mapped[str | None] = mapped_column(String(300), nullable=True)
    
    books: Mapped[List['Book']] = relationship("Book", back_populates="author")
    
    def __str__(self):
        return self.name
    
class Book(Base):
    __tablename__ = 'books'
    
    title : Mapped[str] = mapped_column(String(255), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'), nullable=False)
    isbn : Mapped[str] = mapped_column(String(20), unique=True)
    total_copies : Mapped[int] = mapped_column(Integer, default=1)
    
    author : Mapped['Author'] = relationship("Author", back_populates="books")
    borrowed_books : Mapped[List['MemberBook']] = relationship("MemberBook", back_populates="book")
    
    # deleted borrowed_copies property to avoid N+1 problem 
    # all calculations moved to repository layer

    def __str__(self):
        return self.title


class Member(Base):
    __tablename__ = 'members'
    
    username: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(20))
    joined_date: Mapped[date] = mapped_column(Date, default=date.today)
    
    member_books: Mapped[List["MemberBook"]] = relationship(back_populates="member", lazy="selectin")


class MemberBook(Base):
    __tablename__ = 'member_books'
    
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    member_id: Mapped[int] = mapped_column(ForeignKey('members.id'))
    borrowed_date: Mapped[date] = mapped_column(Date, default=date.today)
    due_date: Mapped[date] = mapped_column(Date)
    returned_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    late_fee: Mapped[float] = mapped_column(DECIMAL(6, 2), default=0.00)
    
    book: Mapped["Book"] = relationship(back_populates="member_books", lazy="joined")
    member: Mapped["Member"] = relationship(back_populates="member_books", lazy="joined")
    
    @property
    def is_returned(self):
        return self.returned_date is not None
    
    @property
    def is_overdue(self):
        if self.is_returned:
            return False
        return date.today() > self.due_date
    
    @property
    def days_overdue(self):
        if not self.is_overdue:
            return 0
        return (date.today() - self.due_date).days