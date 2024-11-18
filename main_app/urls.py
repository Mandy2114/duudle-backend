from django.urls import path
from .views import Home, CreateUserView, LoginView, VerifyUserView, GameDetails, WordList, WordDetail,WordGame


urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('users/register/',CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refesh'),
  path('games/<int:game_id>/', GameDetails.as_view(), name='Game-Details'),
  path('words/', WordList.as_view(), name='word-list'),
  path('words/<int:word_id>/', WordDetail.as_view(), name='word-list'),
  path('words/<int:word_id>/game', WordGame.as_view(), name='Word-Game') 
]