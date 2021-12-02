from shirt import *
from hat import *
from jacket import *
from cowbell import *

def add_to_cart(username):
    item_id = input("Enter item id: ")
    try:
        underscore_index = item_id.index("_")
        category = item_id[:underscore_index]

        quantity = input("Enter the number to add (pos number): ")
        try:
            quantity = int(quantity)
            if (quantity == 0):
                is_zero = True
        except:
            pass
        while not quantity.isdigit() or is_zero:
            is_zero = False
            quantity = input("Enter the number to add (pos number): ")
            try:
                quantity = int(quantity)
                if (quantity == 0):
                    is_zero = True
            except:
                pass

        if category == "shirt":
            item = Shirt(username, item_id, quantity)
        elif category == "hat":
            item = Hat(username, item_id, quantity)
        elif category == "jacket":
            item = Jacket(username, item_id, quantity)
        elif category == "cowbell":
            item = Cowbell(username, item_id, quantity)
        else:
            print("Item does not exist")
            return

        added_items = item.add_item()

        if added_items == quantity:
            print("Successfully added items")
        elif added_items < quantity and added_items != 0:
            print("Not enough stock to add all items! Added " + str(added_items) + " items")
        elif added_items == 0:
            print("Item is out of stock!")
        else:
            print("Item does not exist")
    except:
        print("Item does not exist")

def remove_from_cart(username):
    item_id = input("Enter item id: ")
    try:
        underscore_index = item_id.index("_")
        category = item_id[:underscore_index]

        quantity = input("Enter the number to remove (pos number): ")
        try:
            quantity = int(quantity)
            if (quantity == 0):
                is_zero = True
        except:
            pass
        while not quantity.isdigit() or is_zero:
            is_zero = False
            quantity = input("Enter the number to add (pos number): ")
            try:
                quantity = int(quantity)
                if (quantity == 0):
                    is_zero = True
            except:
                pass
        
        if category == "shirt":
            item = Shirt(username, item_id, quantity)
        elif category == "hat":
            item = Hat(username, item_id, quantity)
        elif category == "jacket":
            item = Jacket(username, item_id, quantity)
        elif category == "cowbell":
            item = Cowbell(username, item_id, quantity)
        else:
            print("Item does not exist")
            return
        
        removed_items = item.remove_item()
        if removed_items == quantity:
            print("Removed all requested items")
        elif removed_items < quantity and removed_items != -1:
            print("You requested to remove more than was in the cart. Removed max possible items from cart")
        else:
            print("Item not in cart")

    except:
        print("Item does not exist")
        

        

