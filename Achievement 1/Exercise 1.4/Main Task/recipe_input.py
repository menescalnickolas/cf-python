import pickle

recipes_list = []
ingredients_list = []

def take_recipe():
  name = str(input("Recipe's name: "))
  cooking_time = int(input("Cooking time in minutes: "))
  ingredients = list(input("Ingredients: ").split(", "))
  difficulty = calc_difficulty()
  recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients, 'difficulty': difficulty}
  calc_difficulty()
  return recipe

def calc_difficulty():
  for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
      recipe["difficulty"] = "Easy"
  
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
      recipe["difficulty"] = "Medium"

    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
      recipe["difficulty"] = "Intermediate"

    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
      recipe["difficulty"] = "Hard"


file_name = input("Filename: ")

try: 
  file = open(file_name, "rb")
  data = pickle.load(file)
  print("File loaded successfully!")

except FileNotFoundError: 
  print("File doesn't exist. We'll create a new file.")
  data = {"recipes_list": [], "all_ingredients": []}

except:
  print("Unexpected error.")
  data = {"recipes_list": [], "all_ingredients": []}

else: 
  file.close()

finally: 
  recipes_list = data["recipes_list"]
  all_ingredients = data["all_ingredients"]


n = int(input("How many recipes would you like to enter?"))

for i in range(n): 
  recipe = take_recipe()
  
  for ingredient in recipe["ingredients"]:
    if not ingredient in ingredients_list:
      ingredients_list.append(ingredient)

  recipes_list.append(recipe)

data = {"recipes_list": recipes_list, "all_ingredients": ingredients_list}

new_filename = open(file_name, "wb")
pickle.dump(data, new_filename)
new_filename.close()