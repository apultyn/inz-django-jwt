from rest_framework import viewsets
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)

from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer


class BookPermission(BasePermission):
    message = "You have to be admin for this operation"

    def has_permission(self, request, _):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="book_admin").exists()
        )

    def has_object_permission(self, request, view, _):
        return self.has_permission(request, view)


class ReviewPermission(BasePermission):
    def has_permission(self, request, _):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="book_admin").exists()
        )

    def has_object_permission(self, request, view, _):
        return self.has_permission(request, view)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [BookPermission]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
