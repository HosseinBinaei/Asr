from django.urls import path
from .views import TimeAPIView, ElapsedAPIView, DateTrackerAPIView

urlpatterns = [
    path("time", TimeAPIView.as_view()),
    path("elapsed/<str:pk>", ElapsedAPIView.as_view()),
    path('waiit/<str:pk>', DateTrackerAPIView.as_view()),
]