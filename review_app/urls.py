from rest_framework.routers import DefaultRouter

from .views import BookViewSet, ReviewViewSet

app_name = "review_app"

router = DefaultRouter()
router.register("books/", BookViewSet)
router.register("reviews/", ReviewViewSet)

urlpatterns = router.urls
