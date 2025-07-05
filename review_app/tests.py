from django.urls import path, include
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from .models import Book


class BookITTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("api/", include("review_app.urls"))]

    def setUp(self):
        self.book1 = Book.objects.create(id="1", title="1984", author="George Orwell")
        self.book2 = Book.objects.create(
            id="2", title="Brave New World", author="Aldous Huxley"
        )

        # self.user = User.objects.create_user(
        #     password="passwd", email="user@example.com"
        # )
        # self.admin = User.objects.create_user(
        #     password="passwd", email="admin@example.com"
        # )

    def test_view_books(self):
        response = self.client.get("/api/books/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_view_book(self):
        response = self.client.get("/api/books/2/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"id": 2, "title": "Brave New World", "author": "Aldous Huxley"},
        )

    def test_create_book_unauth(self):
        response = self.client.post(
            "/api/books/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
