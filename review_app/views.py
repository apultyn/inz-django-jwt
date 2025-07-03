from rest_framework import viewsets
from rest_framework.permissions import AllowAny, BasePermission

from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer


class AdminPermission(BasePermission):
    message = "You have to be admin for this operation"

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.group.filter(name="book_admin").exists()
        )


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects().all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [AdminPermission()]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects().all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [AdminPermission()]
