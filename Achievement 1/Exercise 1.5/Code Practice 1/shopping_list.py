class ShoppingList():
  def __init__(self, list_name):
    self.list_name = list_name
    self.shopping_list = []

  def add_item(self, item):
    if item not in self.shopping_list:
      self.shopping_list.append(item)
      print(item +" added successfully.")
    
    else: 
      print(item + " is already on the list.")

  def remove_item(self, item):
    if item in self.shopping_list:
      self.shopping_list.remove(item)
      print(item + " removed successfully.")
    
    else: 
      print(item + " is not on the list.")

  def view_list(self): 
    if self.shopping_list:
      print(self.list_name)

      for item in self.shopping_list:
        print(item)
    
    else:
      print(self.list_name + " is empty.")

pet_store_list = ShoppingList("Pet Store List")

pet_store_list.add_item("Dog food")
pet_store_list.add_item("Frisbee")
pet_store_list.add_item("Bowl")
pet_store_list.add_item("Collar")
pet_store_list.add_item("Flea collars")


pet_store_list.remove_item("Flea collars")

pet_store_list.add_item("Frisbee")

pet_store_list.view_list()
