from django.test import TestCase
from .models import Recipes

# Create your tests here.
class RecipesModelTest(TestCase):
  def setUpTestData():
    Recipes.objects.create(recipe_id=1, name="Brigadeiro", cooking_time="15", ingredients="Condensed milk, cocoa powder", difficulty="Easy")

  def test_recipe_name(self):
    recipe = Recipes.objects.get(recipe_id=1)
    field_label = recipe._meta.get_field('name').verbose_name
    self.assertEqual(field_label, 'name')

  def test_cooking_time(self):
    recipe = Recipes.objects.get(recipe_id=1)
    self.assertEqual(recipe.cooking_time, 15)

