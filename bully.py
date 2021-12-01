
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import traceback
import logging

# connect to firebase
db_url = "https://bully-py-default-rtdb.firebaseio.com/"
cred = credentials.Certificate("./bully-py_firebase.json")
default_app = firebase_admin.initialize_app(cred, {'databaseURL': db_url})

# reference set to root of database
ref = db.reference("/")

# display help menu
def helpMenu():
    print("\n-----Available commands-----")
    print("1:   /exit    -- exits shop")
    print("2:   /loadNew -- loads a new inventory to the bullypy database (overwrites existing data)")
    print("3:   /viewAll -- view all available items in the store")
    print()

# loads new inventory json file
# NOTE: overwrites existing data in db
# TODO: making this data randomized would be cool
def loadNewInventory():
    try:
        with open("./inventory.json", "r") as f:
            file_contents = json.load(f)
        ref.set(file_contents)
        print("\nNew inventory loaded to firebase!\n")
    except Exception as e:
        print("\nError loading inventory file:")
        logging.error(traceback.format_exc())

# view items in inventory db
def viewAll(arg):
    inventory = ref.get()
    for category in inventory:
        print("\n"+category, end="")
        if arg == 0 or arg == 2:
            print("s:")
            for item in range(len(inventory[category])):
                i = inventory[category][item]
                print("Item ID: "+i["itemID"])
                print("Description: "+i["logoDescription"])
                print("Price: $"+str(i["price"]))
                print("Color: "+str(i["color"]))
                print("Size: "+str(i["size"]))
                print("In Stock: "+str(i["stockNumber"])+"\n")
    if arg == 1:
        print("\n")

# prompt user for login details and verify user with firebase
def login():
    print("Login:")
    newUser = input("Are you a new user (y/n)? ")
    if newUser == "y":
        # TODO: create new user
        print()
        print("New account created!")
    user = input("\nUsername: ")
    pw = input("Password: ")
    # TODO: verify user
    print("\nWelcome <username>!")

# process user commands
def processCmd(ans):
    if ans == "/exit":
        print("Thanks for shopping with us... Goodbye :)")
        return 0
    elif ans == "/help":
        helpMenu()
    elif ans == "/loadNew":
        loadNewInventory()
    elif ans == "/viewAll":
        viewAll(0)
    elif "/viewAll " in ans:
        inventory = ref.get()
        category = ans.split(" ")[1].capitalize()
        if "categories" in ans:
            viewAll(1)
        # category argument can be singular/plural or uppercase/lowercase
        elif category in inventory or category[:len(category)-1] in inventory:
            viewAll(2)
    else:
        print("\n"+ans, "-- not a valid command. Type /help to see a list of commands.\n")

def main():
    print("Welcome to the BullyPy store!")
    print("-----------------------------")
    login()

    print("Enter /help to see list of available commands or /exit to exit the shop")

    while True:
        if processCmd(input("$ ")) == 0:
            return 0

main()
