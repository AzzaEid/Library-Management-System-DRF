from ..models import Author
from ..repository import AuthorRepository

class AuthorManagement:

    @staticmethod
    def get_all_authors():
        return AuthorRepository.get_all_authors()
    
    @staticmethod
    def get_author_by_id(author_id):
        try:
            return AuthorRepository.get_author_by_id(author_id=author_id)
        except Author.DoesNotExist:
            return None
    
    @staticmethod
    def create_author(data):
        return AuthorRepository.create_author(**data)
    
    @staticmethod
    def update_author(author_id, data):
        author = AuthorManagement.get_author_by_id(author_id)
        if not author:
            return None
        author = AuthorRepository.update_author(author, data)
        return author
    
    @staticmethod
    def delete_author(author_id):
        author = AuthorManagement.get_author_by_id(author_id)
        if not author:
            return False
        AuthorRepository.delete_author(author)
        return True
    
    