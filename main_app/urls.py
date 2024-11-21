from django.urls import path
from .views import Home, CreateUserView, LoginView, LogoutView, VerifyUserView, GameDetails, WordList, WordDetail, WordGame, GameList, DrawingList, DrawingDetails


urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('users/register/',CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/logout/', LogoutView.as_view(), name='logout'), 
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refesh'),
  path('games/', GameList.as_view(), name='game-list'), 
  path('games/<int:id>/', GameDetails.as_view(), name='Game-Details'),
  path('words/', WordList.as_view(), name='word-list'), 
  path('words/<int:id>/', WordDetail.as_view(), name='word-list'),
  path('words/<int:id>/games/', WordGame.as_view(), name='Word-Game'), 
  path('games/<int:id>/drawings/', DrawingList.as_view(), name='drawing-list'), 
  path('games/<int:game_id>/drawings/<int:id>/', DrawingDetails.as_view(), name='DrawingDetails'),
  path('games/drawings/', DrawingList.as_view(), name='drawing-list'), 
  path('games/drawings/<int:id>/', DrawingDetails.as_view(), name='DrawingDetails'),
]

