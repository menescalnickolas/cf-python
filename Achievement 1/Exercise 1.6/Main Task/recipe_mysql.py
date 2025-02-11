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