from ..models import Author


class AuthorRepository:
    
    @staticmethod
    def get_all_authors():
        return Author.objects.all()
    
    @staticmethod
    def get_author_by_id(author_id):
        return Author.objects.get(id=author_id)
    
    @staticmethod
    def get_author_with_books(author_id):
        return Author.objects.prefetch_related('book_set').get(id=author_id) # reverse relation
    
    @staticmethod
    def search_authors(query):
        return Author.objects.filter(name=query)
    
    @staticmethod
    def create_author(data):
        return Author.objects.create(**data)
    
    @staticmethod
    def update_author(author, data):
        for key, value in data.items():
            setattr(author, key, value)
        author.save()
        return author
    
    @staticmethod
    def delete_author(author):
        author.delete()

