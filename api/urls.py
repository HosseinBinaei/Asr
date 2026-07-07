from django.urls import path
from .views import TimeAPIView, ElapsedAPIView, NoteListCreateAPIView
from accounts.views import RegisterView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path("time", TimeAPIView.as_view()),
    path("elapsed/", ElapsedAPIView.as_view()),
    path("elapsed/<str:pk>", ElapsedAPIView.as_view()),
    path("note/", NoteListCreateAPIView.as_view()),
    path("note/<str:date>", NoteListCreateAPIView.as_view()),
    path("auth/register/", RegisterView.as_view(), name='register'),
    path("auth/login/", TokenObtainPairView.as_view(), name='login'),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("auth/logout/", TokenBlacklistView.as_view(), name='logout'),
]