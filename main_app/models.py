from django.contrib.auth.models import User
from django.db import models


DIFFICULTY_CHOICES = (
  ('EASY', 'Easy'),
  ('MEDIUM', 'Medium'),
  ('HARD', 'Hard'),
)

class Word(models.Model):
  prompt = models.CharField(max_length=100)
  difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='EASY')

  def __str__(self):
    return self.prompt

class Game(models.Model):
  result = models.BooleanField(default=False) 
  word = models.ManyToManyField(Word) 
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True) 
  difficulty = models.CharField(
    choices=DIFFICULTY_CHOICES, 
    # default=DIFFICULTY_CHOICES[0][0]
    )
  
  def __str__(self): 
    word = self.word.first()
    return f"{word.prompt} | {self.result}"

class Drawing(models.Model):
  game = models.OneToOneField(Game, on_delete=models.CASCADE)
  art = models.TextField()

  def __str__(self):
    return f"Drawing id: {str(self.id)} | Game id: {str(self.game)} "