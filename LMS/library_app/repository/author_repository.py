from ..models.sqlalchemy_models import Author
from ..context.database import Session
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update

class AuthorRepository:

    @staticmethod
    def get_all_authors():
        session = Session()
        stmt = select(Author).options(selectinload(Author.books))
        return session.scalars(stmt).all()

    @staticmethod
    def get_author_by_id(author_id):
        session = Session()
        stmt = select(Author).options(selectinload(Author.books)).where(Author.id == author_id)
        return session.scalar(stmt)
    
    @staticmethod
    def create(data):
        session = Session()
        # author = Author(**data)
        session.add(data)
        session.commit()
        session.refresh(data)
        return data
        
   
    @staticmethod
    def update(author: Author, new_author: Author):
        session = Session()
        author.name = new_author.name
        author.bio = new_author.bio
        session.add(author)
        session.commit()
        session.refresh(author)
        return author

    @staticmethod
    def delete(author):
        session = Session()
        session.delete(author)
        session.commit()

