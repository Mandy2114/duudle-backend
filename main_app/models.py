from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver 
from django.db import models
from django.utils import timezone


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
  
  def delete(self, *args, **kwargs):
    try:
      if hasattr(self, 'drawing'):
        self.drawing.delete()
    except Drawing.DoesNotExist:
      pass
    super().delete(*args, **kwargs)

class Drawing(models.Model):
  game = models.ForeignKey(Game, related_name='drawings', on_delete=models.CASCADE)
  art = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f"Drawing {self.id} for game {self.game_id}"

  class Meta:
      ordering = ['-created_at']


@receiver(pre_delete, sender=User)
def cleanup_user_games(sender, instance, **kwargs):
  Game.objects.filter(user=instance).delete()
