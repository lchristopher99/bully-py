from firebase import firebase
from user import *

def login_screen(user, command):
    if (command == "help"):
        help()
    elif (command == "login"):
        login(user)
    elif (command == "create account"):
        create_account(user)
    else:
        print("Invalid command.")
    print()

def help():
    print("'login': Login to an existing account")
    print("'create account': Create a new account")
    print("'exit': Exit the store")
    print("'help': Display this menu")

def login(user):
    username = input("Enter username: ")
    password = input("Enter password: ")

    correct_password = fb.get("Users/" + username, "password")
    if correct_password == None: # User does not exist
        print("User does not exist")
        return -1
    
    if password != correct_password:
        print("Incorrect password")
        return -1
    
    user.username = username
    user.logged_in = True

def create_account(user):
    username = input("Enter username: ")

    # Check if username is taken
    find_user = fb.get("Users/" + username, None)
    if find_user != None: # Username is taken
        print("Username is taken")
        return -1
    
    password = input("Enter password: ")
    first = input("Enter first name: ")
    last = input("Enter last name: ")
    street = input("Enter street address: ")
    city = input("Enter city: ")
    state = input("Enter state: ")
    zip = input("Enter zip: ")
    card_name = input("Enter credit card name: ")
    card_number = input("Enter credit card number: ")
    security = input("Enter security code: ")
    expiration = input("Enter expiration date: ")

    # Add user to database
    new_user = {
        "password": password,
        "first": first,
        "last": last,
        "shipping": {
            "street": street,
            "city": city,
            "state": state,
            "zip": zip
        },
        "payment": {
            "name": card_name,
            "number": card_number,
            "security": security,
            "expiration": expiration
        },
        "Cart": {
            "cartPrice": 0,
            "cartWeight": 0,
            "numItems": 0
        }
    }
    fb.put("Users", username, new_user)

    # Automatically login upon account creation
    user.username = username
    user.logged_in = True