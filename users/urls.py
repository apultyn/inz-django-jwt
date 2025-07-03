from rest_framework.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserRegister

app_name = "users"

urlpatterns = [
    path("register/", UserRegister.as_view()),
    path("login/", TokenObtainPairView.as_view()),
]
