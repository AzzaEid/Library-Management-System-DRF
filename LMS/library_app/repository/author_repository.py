from ..models import Author


class AuthorRepository:

    @staticmethod
    def get_all_authors():
        return Author.objects.all()

    @staticmethod
    def get_author_with_books(author_id):
        return Author.objects.prefetch_related('book_set').get(id=author_id) # reverse relation
    