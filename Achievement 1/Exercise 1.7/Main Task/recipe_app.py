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
        cooking_time = input('Enter a cooking time in minutes: ')
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

 