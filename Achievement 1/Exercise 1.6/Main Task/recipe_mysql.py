import mysql.connector

conn = mysql.connector.connect(
  host ='localhost',
  user ='cf-python',
  password ='axsydvfcgnhb1!')

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
               id INT PRIMARY KEY AUTO_INCREMENT,
               name VARCHAR(50),
               ingredients VARCHAR(255),
               cooking_time INT, 
               difficulty VARCHAR(20)
               )''')

def main_menu(conn, cursor):
  choice = ""

  while(choice != 'quit'):
    print("Main Menu")
    print("======================================================")
    print("What would you like to do? Pick a choice!")
    print("1. Create a new recipe")
    print("2. Search for a recipe by ingredient")
    print("3. Update an existing recipe")
    print("4. Delete a recipe")
    print("Type 'quit' to exit the program.")
    choice = input("Your choice: ").strip().lower()

    print()

    if choice in ["1", "2", "3", "4"]:

            if choice == "1":
                create_recipe(conn, cursor)
            elif choice == "2":
                search_recipe(conn, cursor)
            elif choice == "3":
                update_recipe(conn, cursor)
            elif choice == "4":
                delete_recipe(conn, cursor)

    elif choice == "quit":
        print("Closing the Recipe App now!")
        break
    
    else: 
        print("Unexpected error! Pick an option or enter 'quit'.")

    conn.commit()

def create_recipe(conn, cursor):
    #Lets user insert values for new recipe
    name = str(input("Recipe name: "))
    cooking_time = int(input("Cooking time in minutes: "))
    ingredients_input = (input("Ingredients: "))
    ingredients = ingredients_input.split(", ")
    difficulty = calculate_difficulty(cooking_time, ingredients)

    ingredients_string = ", ".join(ingredients)

    insert_query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (name, ingredients_string, cooking_time, difficulty))
    conn.commit()

    print("Recipe added succesfully!")


def calculate_difficulty(cooking_time, ingredients):
    ingredients = len(ingredients)
    if cooking_time < 10 and ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and ingredients < 4:
        return "Intermediate"
    elif cooking_time >= 10 and ingredients >= 4:
        return "Hard"


def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    
    #Adds each ingredient into all_ingredients
    all_ingredients = set()
    for row in results: 
        ingredients = row[0]
        ingredients_list = [ingredient.lower().strip() for ingredient in ingredients.split(",")]
        all_ingredients.update(ingredients_list)

    #Display unique ingredients found so far to user and allow them to pick a number corresponding to the ingredient 
    print("Ingredients available: ")
    for i, ingredient in enumerate(sorted(all_ingredients), start=1):
        print(f"{i}. {ingredient}")

    #Allow user to pick a number corresponding to the ingredient in order to search for it
    choice = int(input("Choose an ingredient by number: ")) - 1 #Added -1 because list starts at 1 instead of 0

    #Stores ingredient searched into variable
    search_ingredient = sorted(all_ingredients)[choice]

    #To search for rows in the table that contain search_ingredient
    search_query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    cursor.execute(search_query, ('%' + search_ingredient + '%',))
    search_results = cursor.fetchall()

    if search_results:
        for row in search_results:
            print(row)
    
    else: 
        print("No recipes with this ingredient.")
    

def update_recipe(conn, cursor):
    #Fetches all the recipes in the database with id and name
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()

    #Show recipes to user 
    print("Recipes available to update: ")
    for row in recipes: 
        print(f"ID: {row[0]}, Name: {row[1]}")

    #Let user pick a recipe by id and choose what column to update
    recipe_id = int(input("Enter recipe's ID to update: "))
    column = str(input("What column would you like to update? (name, ingredients or cooking_time)"))

    #Collecting the new value from the user
    new_value = None

    if column == "name":
        new_value = str(input("Enter recipe's new name: "))
        updated_query = "UPDATE Recipes SET name = %s WHERE id = %s"
        cursor.execute(updated_query, (new_value, recipe_id))

    elif column == "ingredients":
        new_value = input("Enter new ingredients separated by comma: ")
        updated_query = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
        cursor.execute(updated_query, (new_value, recipe_id))

    elif column == 'cooking_time':
        new_value = int(input("Enter the new cooking time (in minutes): "))
        update_query = "UPDATE Recipes SET cooking_time = %s WHERE id = %s"
        cursor.execute(update_query, (new_value, recipe_id))

    else: 
        print("Unexpected error.")
        return
    
    #Updating difficulty after user updated values
    if column in ['ingredients', 'cooking_time']:
        cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        row = cursor.fetchone()
        difficulty = calculate_difficulty(row[0], row[1])
        updated_query = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
        cursor.execute(updated_query, (difficulty, recipe_id))

    conn.commit()
    print("Recipe updated!")

def delete_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()

    #Display every recipe in the table
    print("Recipes available: ")
    for row in recipes:
        print(f"ID: {row[0]}, Name: {row[1]}")

    #Lets user pick a recipe by id to delete
    recipe_id = int(input("Pick a recipe by id to delete: "))

    #Query with DELETE statement 
    delete_query = "DELETE FROM Recipes WHERE id = %s"
    cursor.execute(delete_query, (recipe_id,))

    conn.commit()

    print("Recipe deleted!")
    


#Calling main_menu in the main code, passing conn and cursor so it can access the database
try:
    main_menu(conn, cursor)
finally:
    cursor.close()
    conn.close()