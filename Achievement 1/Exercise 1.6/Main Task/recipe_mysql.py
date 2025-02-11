import mysql.connector

conn = mysql.connector.connect(
  host ='localhost',
  user ='cf-python',
  password ='password')

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
               id INT PRIMARY KEY AUTO_INCREMENT,
               name TEXT VARCHAR(50),
               ingredients TEXT VARCHAR(255),
               cooking_time INT, 
               difficulty TEXT VARCHAR(20)
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
    conn.close()
