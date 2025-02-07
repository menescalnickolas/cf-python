import pickle

recipes_list = []

def display_recipe(recipe):
  #To display recipe information
  for recipe in recipes_list: 
    print("Recipe: ", recipe["name"])
    print("Cooking time: ", recipe["cooking_time"])
    print("Ingredients: ", recipe["ingredients"])
    print("Difficulty level: ", recipe["difficulty"])

def search_ingredient(data):
  total_ingredients = enumerate(data["all_ingredients"])
  list_with_numbers = list(total_ingredients)

  print(list_with_numbers)
  
  try: 
    number = int(input("What ingredient are you looking for? Enter its correspondent number: "))
    ingredient_searched = list_with_numbers[number][1]
    
  except: 
    print("Not a valid input.")

  else: 
    for ingredient in data["recipes_list"]:
      if ingredient_searched in ingredient["ingredients"]:
        print(ingredient)

file_name = input("Filename: ")

try: 
  file = open(file_name, "rb")
  data = pickle.load(file)
  print("File loaded successfully!")

except FileNotFoundError: 
  print("File doesn't exist.")

else: 
  file.close()
  search_ingredient(data)