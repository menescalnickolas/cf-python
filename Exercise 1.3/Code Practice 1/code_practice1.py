number_1 = int(input("First number: "))
number_2 = int(input("Second number: "))
operator = input("Add or subtract: ")

if operator == "+":
  print("The result of you addition is: " + str(number_1 + number_2))

elif operator == "-":
  print("The result of you substraction is: " + str(number_1 - number_2))

else: 
  print("Unknown operator.")