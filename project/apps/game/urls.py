from django.urls import path

from game import views as game_views

urlpatterns = [
    path('page/index', game_views.IndexPageView.as_view()),
]
