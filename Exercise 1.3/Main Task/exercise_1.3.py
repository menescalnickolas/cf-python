recipes_list = []
ingredients_list = []


def take_recipe():
  name = str(input("Recipe's name: "))
  cooking_time = int(input("Cooking time in minutes: "))
  ingredients = list(input("Ingredients: ").split(", "))
  recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}



n = int(input("How many recipes would you like to enter?"))

for i in range(n): 
  recipe = take_recipe()
  
  #Checks if ingredient is not on the list
  for ingredient in recipe["ingredients"]:
    if not ingredient in ingredients_list:
      ingredients_list.append(ingredient)

  recipes_list.append(recipe)

#To check recipe's difficulty
for recipe in recipes_list:
  if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
    recipe["difficulty"] = "Easy"
  
  elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
    recipe["difficulty"] = "Medium"

  elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
    recipe["difficulty"] = "Intermediate"

  elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
    recipe["difficulty"] = "Hard"

#To display recipe information
for recipe in recipes_list: 
  print("Recipe: ", recipe["name"])
  print("Cooking time: ", recipe["cooking_time"])
  print("Ingredients: ", recipe["ingredients"])
  print("Difficulty level: ", recipe["difficulty"])

#Function to display all ingredients across all recipes
def all_ingredients():
  print("Ingredients Available Across All Recipes")
  ingredients_list.sort()
  print(ingredients_list) 

all_ingredients()