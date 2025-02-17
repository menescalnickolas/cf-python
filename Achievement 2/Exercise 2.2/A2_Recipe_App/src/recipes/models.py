from django.db import models

# Create your models here.
difficulty_choice = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Intermediate', 'Intermediate'),
    ('Hard', 'Hard'),
)

class Recipes(models.Model):
  recipe_id = models.PositiveIntegerField()
  name = models.CharField(max_length=50)
  cooking_time = models.PositiveIntegerField(help_text='in minutes')
  ingredients = models.TextField()
  difficulty = models.CharField(max_length=12, choices=difficulty_choice)
  
  def __str__(self):
    return str(self.name)