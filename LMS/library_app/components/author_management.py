# from ..models.django_orm import Author
from ..repository import AuthorRepository
from rest_framework.exceptions import ValidationError
class AuthorManagement:
    def __init__(self, **kwargs):
        self.auther_repo = AuthorRepository()
        super().__init__(**kwargs)
        
        
    def get_all_authors(self):
        return self.auther_repo.get_all_authors()
    
    def get_author_by_id(self,author_id):
        try:
            return self.auther_repo.get_author_by_id(author_id=author_id)
        except :
            raise ValidationError({"auther": "auther with id doesn't exist"})
    
    def create_author(self, data):
        return self.auther_repo.create(**data)
    
    def update_author(self, author_id, data):
        author = self.auther_repo.get_author_by_id(author_id)
        if not author:
            return None
        author = self.auther_repo.update(author, data)
        return author
    
    def delete_author(self,author_id):
        author = self.get_author_by_id(author_id)
        if not author:
            return False
        self.auther_repo.delete(author)
        return True
    
    