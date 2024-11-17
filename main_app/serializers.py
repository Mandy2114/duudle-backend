from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Game, Drawing, Word

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    field = ('id', 'username', 'email', 'password')

  def create(self, validated_data):
    user = User.objects.create_user(
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password']
    )

    return user 

class GameSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(read_only=True)
  class Meta:
    model = Game
    field = '__all__'
    
# Word serializer
class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'