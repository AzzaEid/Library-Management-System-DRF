from rest_framework import serializers
from LMS.library_app.models.django_orm.author import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']

