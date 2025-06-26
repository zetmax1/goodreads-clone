
from rest_framework import serializers

from books.models import Book, BookReview
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'isbn')


class BookReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    author = UserSerializer(read_only=True)

    author_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookReview
        fields = ('id', 'stars_given', 'comment', 'book', 'author', 'author_id', 'book_id')