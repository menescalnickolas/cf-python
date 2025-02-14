#Importing all necessary packages and methods
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

#Engine object that connects to database
engine = create_engine("mysql://cf-python:axsydvfcgnhb1!@localhost/task_database")

#Storing declarative base class into variable called "Base"
Base = declarative_base()

#Session object that will make changes to database
Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
  __tablename__ = "recipes" #Attribute to set the table's name

  #Attributes to create columns in my table
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  ingredients = Column(String(255))
  cooking_time = Column(Integer)
  difficulty = Column(String(20))

  #This method shows a quick representation of the recipe
  def __repr__(self):
    return f"<Recipe ID: {self.id} - Name: {self.name} - Difficulty: {self.difficulty}>"
  
  #This method prints the recipe
  def __str__(self):
    return (
      f"{"="*10}\n"
      f"Recipe ID: {self.id}\n"
      f"Recipe: {self.name}\n"
      f"Cooking Time: {self.cooking_time} minutes\n"
      f"Ingredients: {self.ingredients}\n"
      f"Difficulty: {self.difficulty}\n"
      f"{"="*10}\n"
    )
    

  #This method calculates the difficulty of the recipe based on number of ingredients and cooking time
  def calculate_difficulty(self, cooking_time, ingredients):
    ingredients = len(ingredients)
    if cooking_time < 10 and ingredients < 4:
        self.difficulty = "Easy"
    elif cooking_time < 10 and ingredients >= 4:
        self.difficulty = "Medium"
    elif cooking_time >= 10 and ingredients < 4:
        self.difficulty = "Intermediate"
    elif cooking_time >= 10 and ingredients >= 4:
        self.difficulty = "Hard"


  #This method retrieves the ingredients string inside the recipe object as a list
  def return_ingredients_as_list(self):
     if not self.ingredients:  
        print("There are no ingredients to display.")
        return []
     else:
        print("Here are your ingredients: ")
        return self.ingredients.split(', ')
     
#Creates the table on the database     
Base.metadata.create_all(engine)

#ESTABLISHING THE FUNCTIONS TO BE EXECUTED IN MAIN MENU

def create_recipe():
   #While loop to get the recipe's name from the user
  while True:
    name = input('Enter the recipe\'s name (max. 50 characters): ')
    if len(name) > 50:
      print("Error: Name contains more than 50 characters. Please, make sure your recipe\'s name contains less than 50 characters.")
    elif not name.isalpha():
      print("Error: Name can only contain letters.")
    else:
      break
  
  #While loop to get cooking time from the user
  while True:
        cooking_time = input("Enter cooking time in minutes: ")
        if not cooking_time.isnumeric():
            print("Error: Cooking time must be a number. Try again.")
        else:
            cooking_time = int(cooking_time)
            break


  #Getting ingredients from the user    
  ingredients = [] #Temporary list of ingredients
  number_of_ingredients = int(input("How many ingredients does your recipe have?"))

  for i in range (number_of_ingredients):
     ingredient = input("Enter the name of the ingredient: ")
     ingredients.append(ingredient) #Adds ingredient to the temporary list

  #Converts the list of ingredients into string, each ingredient is joined with a comma
  ingredients_str = ", ".join(ingredients) 

   # Create new Recipe object
   # Create new Recipe object
  recipe_entry = Recipe(
    name = name,
    cooking_time = cooking_time,
    ingredients = ingredients_str
    )
  
  #Generates the difficulty attribute for this new recipe
  recipe_entry.calculate_difficulty()

  #Adds new recipe to the database
  session.add(recipe_entry)
  session.commit()

  print({Recipe.name} + " has been added to the list of recipes!")


def view_all_recipes():
   #Retrieves all recipes from the database as a list
   recipes_list = session.query(Recipe).all()

   #Informs the user that there are no recipes in the database and exits the funtion to return to the main menu
   if not recipes_list:
    print("There are currently no recipes in the database.")
    return None
   
   #Displays all recipes in the database to the user
   for recipe in recipes_list:
      print(recipe)

def search_by_ingredients():
   #Checks if there are any recipes in the database
   recipe_count = session.query(Recipe).count()

   #If there are no entries, notify the user and exit the function
   if recipe_count == 0:
    print("There are no recipes in the database.")
    return None
   
   #Retrieves values from the ingredients column and stores in variable "results"
   results = session.query(Recipe.ingredients).all()

   #Initialize temporary empty list
   all_ingredients = []

   for result in results:
      #Goes through each entry in results and splits the ingredients into temporary list
      ingredients_list = result[0].split(', ')
      
      #Check if ingredient is already in the list, if not add it to the list
      for ingredient in ingredients_list:
         if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)
      
      #Displays all ingredients (numbered) available to the user with each ingredient 
      print("Available ingredients: ")
      for idx, ingredient in enumerate(all_ingredients, start=1): #Adds numbers to the ingredients starting at 1
        print(f"{idx}. {ingredient}")
      
      #Asks user what ingredients to select
      selected_ingredients = input("Enter the correspondent numbers of the ingredients you're looking for. Separate numbers by space: ")
      
      #Checks that the user's inputs match the options available otherwise exit the function and inform the user
      try:
        selected_numbers = [int(i) for i in selected_ingredients.split()]
        
      except ValueError:
        print("Error! Please, enter a valid number.")
        return None
      
      #In case the user enters a number that's not in the list
      if any(i < 1 or i > len(all_ingredients) for i in selected_numbers):
         print("Error! Please, enter a number from the list above.")
         return None
      
      #Makes a list of ingredients to be searched for, containing ingredients as strings
      search_ingredients = [all_ingredients[i-1] for i in selected_numbers]

      #Initializes empty list "conditions"
      conditions = []

      #Loop that runs through search_ingredients
      for i in search_ingredients:
        like_term = f'%{i}%' #Search string
        conditions.append(Recipe.ingredients.like(like_term)) #Appends the search condition with the like_term

      #Retrieves all recipes from database using filter() that contains the conditions, and displays the recipes
      results = session.query(Recipe).filter(*conditions).all()
      
      if results:
         for recipe in results:
            print(recipe)
      else:
         print("There are no recipes with these ingredients.")

def edit_recipe():
   #Checks if there are any recipes in the database
   recipe_count = session.query(Recipe).count()

   #Continues only if there are any recipes, otherwise exit function
   if recipe_count == 0:
    print("There are no recipes in the database.")
    return None
   
   #Retrieves id and name for each recipe and stores them in "results"
   results = session.query(Recipe.id, Recipe.name).all()

   print("Recipes available to be edited: ")
   
   for recipe in results:
    print(f"ID: {recipe.id} - Name: {recipe.name}") #Display recipes to the user
    
  #Lets user pick a recipe by ID - if ID is invalid, exit the function
    selected_recipe = input("Enter the ID of the recipe you'd like to edit: ")
    if not selected_recipe.isnumeric() or int(selected_recipe) not in [r.id for r in results]::
    print("The ID is invalid!")
    return None
   
   #Retrieves the entire recipe that corresponds with ID into variable "recipe_to_edit"
   recipe_to_edit = session.query(Recipe).filter_by(id=int(selected_recipe)).one()

   #Display recipe to the user and lets the user pick a number corresponding to an attribute
   print("==========")
   print("Recipe information:")
   print(f"1. Name: {recipe_to_edit.name}")
   print(f"2. Ingredients: {recipe_to_edit.ingredients}")
   print(f"3. Cooking Time: {recipe_to_edit.cooking_time} minutes")
   print("==========")
   
   choice = input("Enter the corresponding number of the attribute you'd like to edit (1, 2 or 3): ")

   #Checks user input
   if choice not in ['1', '2', '3']:
      print("Enter a valid option (1, 2 or 3)!")
      return None
   
   #Proceed with editing the attributes
   #If user chooses to edit recipe's name
   if choice == "1":
    edited_name = input("Editing recipe's name. What's the updated name of your recipe?: ")
    if len(edited_name) > 50 or not edited_name.isalpha():
        print("Error! Recipe's name must have 50 characters or less.")
        return None
    recipe_to_edit = edited_name
   
   #If user chooses to edit recipe's ingredients
   elif choice == "2":
      edited_ingredients = []
      number_of_ingredients = int(input("How many ingredients does your recipe have?"))
      
      for i in range (number_of_ingredients):
         ingredient = input("Enter the name of the ingredient: ")
         edited_ingredients.ingredients.append(ingredient) #Adds ingredient to the temporary list
      
      #Converts the list of ingredients into string, each ingredient is joined with a comma   
      recipe_to_edit.ingredients = ", ".join(edited_ingredients) 

  #If user chooses to edit recipe's cooking time
   elif choice == "3":
      edited_cooking_time = input("Enter cooking time in minutes: ")
      if not edited_cooking_time.isnumeric():
            print("Error: Cooking time must be a number. Try again.")
            return None
      recipe_to_edit.cooking_time = int(edited_cooking_time)
      
   #Recalculates recipe's difficulty based on new input 
   recipe_to_edit.calculate_difficulty()  
  
   session.commit()

   print("Recipe has been edited successfully!")

def delete_recipe():
   

    
   







   





           
         

      
   

