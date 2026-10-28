from django.urls import path

from .views import QuizResultView, QuizView, RoomCreateView, RoomDetailView, RoomVoteView

urlpatterns = [
    path("quiz/", QuizView.as_view()),
    path("quiz/result/", QuizResultView.as_view()),
    path("rooms/", RoomCreateView.as_view()),
    path("rooms/<str:code>/", RoomDetailView.as_view()),
    path("rooms/<str:code>/vote/", RoomVoteView.as_view()),
]