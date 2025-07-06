from rest_framework import serializers
from .models import Book, Review


class ReviewSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source="author.email", read_only=True)

    class Meta:
        model = Review
        fields = ("id", "stars", "comment", "author_email", "book")


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ("id", "title", "author", "reviews")
