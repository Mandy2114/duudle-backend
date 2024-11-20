from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Game, Drawing, Word

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'password')

  def create(self, validated_data):
    user = User.objects.create_user(
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password']
    )

    return user 

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'

class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(read_only=True)
  word = WordSerializer(many=True, read_only=True)
  difficulty = serializers.CharField(read_only=True)  # Make difficulty read-only

  class Meta:
    model = Game
    fields = '__all__'

  def create(self, validated_data):
        # Set difficulty based on the word
    word_list = validated_data.get('word', [])
    if word_list:
            # Set the game's difficulty based on the first word's difficulty
      validated_data['difficulty'] = word_list[0].difficulty  # Get the first word's difficulty
        
    return super().create(validated_data)
