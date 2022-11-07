from rest_framework import serializers
from rest_framework.generics import ListAPIView

from data.models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'created', 'updated', 'isbn', 'title', 'published']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'created', 'updated', 'book_set']

    book_set = BookSerializer(many=True, read_only=True)


class BasicAuthorListView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
