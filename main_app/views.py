from .serializers import UserSerializer, GameSerializer, WordSerializer, DrawingSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, logout
from rest_framework.exceptions import PermissionDenied
from .models import Game, Word, Drawing
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import JsonResponse
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import requests
import base64
import os

load_dotenv()
VITE_GROQ_API_KEY = os.getenv("VITE_GROQ_API_KEY")

class Home(APIView):

  def get(self, request):
    content = {'message': 'welcome to Whataduudle'}
    return Response(content)

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv  USER VIEWS  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *arg, **kwargs):
    response = super().create(request, *arg, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
    'refresh': str(refresh),
    'access': str(refresh.access_token),
    'user': response.data
  }) 

class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
  
class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            # Clean up user's unfinished games
            Game.objects.filter(
                user=request.user,
                result=False
            ).delete()
            
        logout(request)
        return Response(status=status.HTTP_200_OK)
    def post(self, request):
        if request.user.is_authenticated:
            # Clean up user's unfinished games
            Game.objects.filter(
                user=request.user,
                result=False
            ).delete()
            
        logout(request)
        return Response(status=status.HTTP_200_OK)

class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]
  def get(self, request):
    user = User.objects.get(username=request.user)
    refresh = RefreshToken.for_user(request.user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv  GAME VIEWS  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
class GameList(generics.ListCreateAPIView):
  serializer_class = GameSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    # This ensures we only return Games belonging to the logged-in user
    user = self.request.user
    print(user)
    return Game.objects.filter(user=user)


# Gets the Game details | games/<int:id>/
class GameDetails(generics.RetrieveUpdateDestroyAPIView):
  queryset = Game.objects.all()
  fields = '__all__'
  lookup_field = 'id'
  serializer_class = GameSerializer

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    word_associated_with_game = Word.objects.filter(id__in=instance.word.all())
    word_serializer = WordSerializer(word_associated_with_game, many=True)

    return Response({
      'game': serializer.data,
      'word_associated_with_game': word_serializer.data  
    })
  
  def partial_update(self, request, *args, **kwargs):
    # Get the game object by game_id from the URL
    game = self.get_object()

    # Check if "word_id" is in the request data
    word_id = request.data.get('word')

    if word_id:
        # If word_id is provided, handle word update and difficulty assignment
        try:
            word = Word.objects.get(id=word_id)
            # Update the game's associated word
            game.word.set([word])
            # Automatically update the game's difficulty to match the word's difficulty
            game.difficulty = word.difficulty
            game.result = False
            game.save()

        except Word.DoesNotExist:
            return Response({"error": "Word not found."}, status=status.HTTP_404_NOT_FOUND)

    # If "word_id" is not in the request data, process the normal PATCH update
    serializer = self.get_serializer(game, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()  # Save other changes to the game
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv  WORD VIEWS  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# Word Library
class WordList(generics.ListCreateAPIView):
  queryset = Word.objects.all()
  serializer_class = WordSerializer
  
# Retrieves a Single Word Details
class WordDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Word.objects.all()
  serializer_class = WordSerializer
  lookup_field = 'id'
  
# Create an the game for the user.
class WordGame(generics.CreateAPIView):
  serializer_class = GameSerializer
  permission_classes = [IsAuthenticated]

  def perform_create(self, serializer):
    user = self.request.user
    word_id = self.kwargs['id']
    word = Word.objects.get(pk=word_id)
    game_difficulty = word.difficulty
    serializer.save(user=user,word=[word], difficulty=game_difficulty)
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv  DRAWING VIEWS  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# List out all the Drawings | games/<int:id>/drawings/
class DrawingList(generics.ListCreateAPIView):
  serializer_class = DrawingSerializer

  def get_queryset(self):
      game_id = self.kwargs.get('game_id')
      return Drawing.objects.filter(game_id=game_id)

  def perform_create(self, serializer):
      game_id = self.kwargs.get('game_id')
      serializer.save(game_id=game_id)

  def post(self, request, *args, **kwargs):
      try:
          game_id = self.kwargs.get('game_id')
            # Add game_id to request data
          request.data['game'] = game_id
          return super().post(request, *args, **kwargs)
      except Exception as e:
          return Response(
              {"error": str(e)},
              status=status.HTTP_500_INTERNAL_SERVER_ERROR
          )

# Retreive, Update and Delete Drawings | 'games/<int:game_id>/drawings/<int:id>/'
class DrawingDetails(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = DrawingSerializer
  lookup_field = 'pk'  # This should match the URL parameter name

  def get_queryset(self):
      game_id = self.kwargs.get('game_id')
      return Drawing.objects.filter(game_id=game_id)

  def update(self, request, *args, **kwargs):
      try:
          instance = self.get_object()
          serializer = self.get_serializer(instance, data=request.data, partial=True)
            
          if serializer.is_valid():
              self.perform_update(serializer)
              return Response(serializer.data)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
      except Exception as e:
          return Response(
              {"error": str(e)},
              status=status.HTTP_500_INTERNAL_SERVER_ERROR
          )

