from firebase import firebase
from user import User
from shirt import Shirt
from jacket import Jacket
from hat import Hat
from cowbell import Cowbell

db_url = "https://groupproject-8d2e6-default-rtdb.firebaseio.com/"
fb = firebase.FirebaseApplication(db_url, None)

def store_screen(user, command):
    if (command == "help"):
        help()
    elif (command == "display shirts"):
        shirt = Shirt()
        shirt.display()
    elif (command == "display jackets"):
        jacket = Jacket()
        jacket.display()
    elif (command == "display hats"):
        hat = Hat()
        hat.display()
    elif (command == "display cowbells"):
        cowbell = Cowbell()
        cowbell.display()
    elif (command == "edit payment"):
        card_number = input("Enter new credit card number: ")
        card_name = input("Enter new credit card name: ")
        card_security = input("Enter new security code: ")
        card_expiration = input("Enter expiration date: ")
        user.edit_payment(card_number, card_name, card_security, card_expiration)
    elif (command == "edit shipping"):
        street_address = input("Enter new street address: ")
        city = input("Enter new city: ")
        state = input("Enter new state: ")
        zip = input("Enter new zip code: ")
        user.edit_shipping(street_address, city, state, zip)
    elif (command == "add item"):
        add_item(user)
    elif (command == "remove item"):
        remove_item(user)
    elif (command == "checkout"):
        checkout(user)
    elif (command == "display cart"):
        display_cart(user)
    elif (command == "display orders"):
        display_orders(user)
    elif (command == "delete account"):
        delete_account(user)
    elif (command == "logout"):
        print("Logging out")
        user.clear_cart()
        user.logged_in = False
    else:
        print("Invalid command")
    print()

def help():
    print("'display <shirts/jackets/hats/cowbells>' : Displays all items in the specified category")
    print("'display orders'                         : Displays order history")
    print("'display cart'                           : Displays cart")
    print("'edit <payment/shipping>'                : Edit payment or shipping information")
    print("'add item'                               : Add an item to your cart")
    print("'remove item'                            : Remove an item from your cart")
    print("'checkout'                               : Checkout with the current items in the cart")
    print("'logout'                                 : Logout of your account")
    print("'delete account'                         : Delete your account")
    print("'help'                                   : Display this menu")

def add_item(user):
    valid_input = False

    item_id = input("Enter the item id of the item you want to add: ")
    # Loop until positive integer is entered
    while not valid_input:
        quantity = input("Enter the quantity of the item id (positive integer): ")
        try:
            quantity = int(quantity)
            if quantity > 0:
                valid_input = True
        except:
            pass
    
    added_items = user.add_to_cart(item_id, quantity)
    if (added_items == -1):
        print("Item does not exist")
    elif (added_items == 0):
        print("Item is out of stock")
    elif (added_items == quantity):
        print("Added the items to your cart")
    else:
        print("Not enough stock to add all requested items. Added " + str(added_items) + " items")

def remove_item(user):
    valid_input = False

    item_id = input("Enter the item id of the item you want to remove: ")
    # Loop until positive integer is entered
    while not valid_input:
        quantity = input("Enter the quantity of the item id (positive integer): ")
        try:
            quantity = int(quantity)
            if quantity > 0:
                valid_input = True
        except:
            pass
    
    removed_items = user.remove_from_cart(item_id, quantity)
    if (removed_items == -1 or removed_items == 0):
        print("Item not in cart")
    elif (removed_items == quantity):
        print("Removed the items from your cart")
    else:
        print("You tried to remove more items than were in your cart. Removed all instances of that item in your cart")

def checkout(user):
    val = user.checkout()
    if val == -1:
        print("No items in cart!")
    else:
        print("Transaction complete!")

def display_cart(user):
    val = user.display_cart()
    if val == -1:
        print("Cart has no items inside")

def display_orders(user):
    val = user.display_orders()
    if val == -1:
        print("No order history")

def delete_account(user):
    confirm = input("Are you sure (y/n): ")
    if (confirm != "y"):
        print("Account deletion cancelled")
        return -1
    
    # Clear cart and restock inventory
    user.clear_cart()

    # Delete account from database
    fb.delete("Users", user.username)

    # Exit from store screen upon deletion
    user.logged_in = False