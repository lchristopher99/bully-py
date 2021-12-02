import json
# database
from firebase_admin import db
# debug
import traceback
import logging

class Inventory:
    # returns current inventory json obj
    def getCurrentInventory():
        ref = db.reference("/")
        return ref.get()["Inventory"]

    # returns referene to database at root
    def getDatabaseRef():
        ref = db.reference("/")
        return ref

    # loads new inventory json file to database ref passed in
    # NOTE: overwrites existing data in db
    # TODO: making this data randomized would be cool
    def loadNewInventory():
        try:
            with open("inv_sys/inventory.json", "r") as f:
                file_contents = json.load(f)
            Inventory.getDatabaseRef().set(file_contents)
            print("\nNew inventory loaded to firebase!\n")
        except Exception as e:
            print("\nError loading inventory file:")
            logging.error(traceback.format_exc())

    # view items in inventory at database ref passed in
    # accepts arguments for viewing all items,
    # viewing individual categories, and viewing all categorie names
    def viewAll(arg):
        for category in Inventory.getCurrentInventory():
            if arg == "all" or arg == "categories" or arg == category:
                print("\n"+category, end="")
            if arg == "all" or arg == category:
                print("s:")
                for item in Inventory.getCurrentInventory()[category]:
                    i = Inventory.getCurrentInventory()[category][item]
                    print("Item ID: "+item)
                    print("Description: "+i["logoDescription"])
                    print("Price: $"+str(i["price"]))
                    print("Color: "+i["color"])
                    print("Size: "+i["size"])
                    print("In Stock: "+str(i["stockNumber"])+"\n")
        if arg == "categories":
            print("\n")
