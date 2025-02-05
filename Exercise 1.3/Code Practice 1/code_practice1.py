number_1 = input("First number: ")
number_2 = input("Second number: ")
operator = input("Add or subtract: ")

if operator == "+":
  print('The result of you addition is:' + number_1 + number_2)

elif operator == "-":
  print('The result of you substraction is:' + number_1 - number_2)

else: 
  print('Unknown operator.')