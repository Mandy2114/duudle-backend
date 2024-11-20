from .serializers import UserSerializer, GameSerializer, WordSerializer, DrawingSerializer, PredictionSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Game, Word, Drawing, Prediction
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
  queryset = Drawing.objects.all()
  serializer_class = DrawingSerializer

  def post(self, request, *args, **kwargs):
    # Get the game_id from the URL
    game_id = kwargs.get('id') 
    try:
        # Fetch the Game object based on game_id
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)
    # Create the drawing data and automatically set the game field
    drawing_data = request.data.copy()  
    drawing_data['game'] = game.id   # Automatically set the game from the URL
    
    # Serialize and validate the data
    serializer = self.get_serializer(data=drawing_data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)

    return Response(serializer.data, status=status.HTTP_201_CREATED)
# Retreive, Update and Delete Drawings | 'games/<int:game_id>/drawings/<int:id>/'
class DrawingDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer
    lookup_field = 'id'
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv  PREDICTIONS VIEWS  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# Single Prection
class PredictionView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def preprocess_image(image_file):
      img = Image.open(image_file).convert("RGB")  # Convert to RGB (not RGBA)
      img.thumbnail((224, 224), Image.ANTIALIAS)  # Resize to thumbnail
      canvas = Image.new("RGB", (224, 224), (255, 255, 255))  # New RGB canvas with white background
      offset = ((224 - img.width) // 2, (224 - img.height) // 2)  # Center the image
      canvas.paste(img, offset)
      
      buffer = BytesIO()
      canvas.save(buffer, format="JPEG")  # Save as JPEG
      return base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    def call_groq_api(base64_image):
      response = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
      headers={
        "Authorization": "Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
      },
      json={
        "model": "llama-3.2-11b-vision-preview",
        "messages": [
          {"role": "user", "content": [
            {"type": "text", "text": "What does this image show?"},
            {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
          ]}
        ],
        "temperature": 0.1,
      },
      )
      return response.json()

    def handle_prediction(request):
      image_file = request.FILES[image] # Uploaded file
      base64_image = preprocess_image(image_file)
      groq_response = call_groq_api(base64_image)
      result = process_prediction_response(groq_response, target_word=cat)
      drawing_id = request.data.get('drawing')  # Assuming drawing ID is passed in request data

        # Fetch the Drawing object based on drawing_id
      try:
        drawing = Drawing.objects.get(id=drawing_id)
      except Drawing.DoesNotExist:
        return Response({"error": "Drawing not found."}, status=status.HTTP_404_NOT_FOUND)
      
      prediction = Prediction.objects.create(
        drawing=drawing,  # Assign the valid Drawing instance
        prediction=result['prediction']
      )
      
      return JsonResponse(result)
    
    def process_prediction_response(response, target_word):
      prediction_text = response[choices][0][message][content]

      is_correct = target_word.lower() in prediction_text.lower()
      confidence = response.get(confidence, 0)
      return {prediction: prediction_text, is_correct: is_correct, confidence: confidence}

    def post(self, request, *args, **kwargs):
        try:
            # Retrieve the uploaded image
            image_file = request.FILES['image']
            
            # Preprocess the image: Resize and encode to Base64
            image = Image.open(image_file)
            image = image.resize((224, 224))  # Resize to 224x224
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

            # Call the Groq API
            groq_api_key = VITE_GROQ_API_KEY
            groq_url = 'https://api.groq.com/openai/v1/chat/completions'

            response = requests.post(
                groq_url,
                headers={
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.2-11b-vision-preview",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "What's in this image?"},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                },
                            ]
                        }
                    ],
                    "temperature": 0.1,
                },
            )

            if response.status_code != 200:
                return Response(
                    {"error": "Failed to get prediction", "details": response.json()},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Extract prediction from Groq API response
            prediction_text = response.json()["choices"][0]["message"]["content"]

            # Save prediction to database (optional)
            prediction = Prediction.objects.create(drawing=image_file, predicted_word=prediction_text)

            # Serialize and return response
            serializer = PredictionSerializer(prediction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
  # game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='prediction')  # Link to a specific game
  # drawing = models.ForeignKey(Drawing, on_delete=models.CASCADE, related_name='predictions')  # Link to a drawing
  # predicted_word = models.CharField(max_length=100)  # The predicted word
  # confidence = models.FloatField()  # Confidence score of the prediction
  # is_correct = models.BooleanField(default=False)  # Whether the prediction matches the word
  # created_at = 