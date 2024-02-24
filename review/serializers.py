from rest_framework import serializers
from .models import Author, Book, Review

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'published_books', 'total_rating', 'author_review_count']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'total_rating', 'book_review_count']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    author = AuthorSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['user', 'author', 'book', 'review_content', 'content', 'rating']
