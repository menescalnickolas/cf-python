class Recipe:

  all_ingredients = set()


  def __init__(self, name, ingredients, cooking_time):
    self.name = name
    self.ingredients = ingredients
    self.cooking_time = cooking_time
    self.difficulty = self.calculate_difficulty()

  def calculate_difficulty(self):
      if self.cooking_time < 10 and len(self.ingredients) < 4:
        return "Easy"
  
      elif self.cooking_time < 10 and len(self.ingredients) >= 4:
        return "Medium"

      elif self.cooking_time >= 10 and len(self.ingredients) < 4:
        return "Intermediate"

      elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
        return "Hard"


  def get_name(self):
    return self.name
  
  def set_name(self, name):
    self.name = name

  def get_cooking_time(self):
    return self.cooking_time
  
  def set_cooking_time(self, cooking_time):
    self.cooking_time = cooking_time

  def add_ingredients(self, *ingredients):
    self.ingredients.extend(ingredients)
    self.update_all_ingredients()

  def get_ingredients(self):
    return self.ingredients
  
  def get_difficulty(self):
    if not self.difficulty:
      self.difficulty = self.calculate_difficulty()
    return self.difficulty
  
  def search_ingredients(self, ingredient):
    return ingredient in self.ingredients
  
  def update_all_ingredients(self):
    Recipe.all_ingredients.update(self.ingredients)

  def __str__(self):
    if not self.ingredients:
      return self.name + ": No ingredients added yet."
    
    else: 
      return f"Recipe Name: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.get_difficulty()}\n"

def recipe_search(data, search_term):
  print("Recipes with: " + search_term)

  for recipe in data:
    if recipe.search_ingredients(search_term):
      print(recipe)


tea = Recipe("Tea", ["Tea Leaves", "Sugar", "Water"], 5)
coffee = Recipe("Coffee", ["Coffee Powder", "Sugar", "Water"], 5)
cake = Recipe("Cake", ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"], 50)
banana_smoothie = Recipe("Banana Smoothie", ["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"], 5)

recipe_list = [tea, coffee, cake, banana_smoothie]

#String Representation to display recipes
for recipe in recipe_list:
  print(recipe)


for ingredient in ["Water", "Sugar", "Bananas"]:
  recipe_search(recipe_list, ingredient)