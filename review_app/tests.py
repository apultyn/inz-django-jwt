from django.urls import path, include
from django.contrib.auth.models import Group

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Book, Review
from users.models import NewUser


class BookITTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("api/", include("review_app.urls"))]

    def setUp(self):
        self.book1 = Book.objects.create(id="1", title="1984", author="George Orwell")
        self.book2 = Book.objects.create(
            id="2", title="Brave New World", author="Aldous Huxley"
        )

        self.user = NewUser.objects.create_user(
            password="passwd", email="user@example.com"
        )
        self.admin = NewUser.objects.create_user(
            password="passwd", email="admin@example.com"
        )

        self.group = Group.objects.create(name="book_admin")
        self.admin.groups.add(self.group)
        self.admin.save()

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

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

    def test_create_book_user(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(
            "/api/books/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_admin(self):
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(
            "/api/books/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book_unauth(self):
        response = self.client.put(
            "/api/books/1/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_user(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.put(
            "/api/books/1/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_admin(self):
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.put(
            "/api/books/1/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book_unauth(self):
        response = self.client.delete(
            "/api/books/1/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_user(self):
        token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(
            "/api/books/1/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_admin(self):
        token = self.get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(
            "/api/books/1/",
            format="json",
            data={"title": "Dune", "author": "Frank Herbert"},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReviewITTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("api/", include("review_app.urls"))]

    def setUp(self):
        self.book1 = Book.objects.create(id="1", title="1984", author="George Orwell")
        self.book2 = Book.objects.create(
            id="2", title="Brave New World", author="Aldous Huxley"
        )

        self.user = NewUser.objects.create_user(
            password="passwd", email="user@example.com"
        )
        self.admin = NewUser.objects.create_user(
            password="passwd", email="admin@example.com"
        )

        self.group = Group.objects.create(name="book_admin")
        self.admin.groups.add(self.group)
        self.admin.save()

        self.review1 = Review.objects.create(
            id="1", stars="5", comment="Awesome book", author=self.user, book=self.book1
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_view_reviews(self):
        response = self.client.get("/api/reviews/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_view_review(self):
        response = self.client.get("/api/reviews/1/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["comment"], "Awesome book")
        self.assertEqual(data["stars"], 5)
