from django.urls import path
from .views import TimeAPIView, ElapsedAPIView, NoteListCreateAPIView

urlpatterns = [
    path("time", TimeAPIView.as_view()),
    path("elapsed/", ElapsedAPIView.as_view()),
    path("elapsed/<str:pk>", ElapsedAPIView.as_view()),
    path("note/", NoteListCreateAPIView.as_view()),
    path("note/<str:date>", NoteListCreateAPIView.as_view()),
]