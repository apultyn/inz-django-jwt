from django.urls import path
from .views import BookViewSet, ReviewViewSet

app_name = "review_app"

urlpatterns = [
    path("books/", BookViewSet, basename="book"),
    path("reviews/", ReviewViewSet, basename="review"),
]
