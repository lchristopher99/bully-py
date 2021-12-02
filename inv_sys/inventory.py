import json
# database
from firebase_admin import db
# debug
import traceback
import logging

class Inventory:
    # returns current inventory json obj
    def getCurrent():
        ref = db.reference("/")
        return ref.get()["Inventory"]

    # returns referene to inventory database
    def getRef():
        ref = db.reference("/Inventory")
        return ref

    # loads new inventory json file to database
    # NOTE: overwrites existing inventory in db
    # TODO: making this data randomized would be cool
    def loadNew():
        try:
            with open("inv_sys/inventory.json", "r") as f:
                file_contents = json.load(f)
            Inventory.getRef().set(file_contents)
            print("\nNew inventory loaded to firebase!")
        except Exception as e:
            print("\nError loading inventory file:")
            logging.error(traceback.format_exc())

    # view items in inventory database
    # accepts arguments for viewing all items,
    # viewing individual categories, and viewing all categorie names
    def viewAll(arg):
        for category in Inventory.getCurrent():
            if arg == "all" or arg == "categories" or arg == category:
                print("\n"+category, end="")
            if arg == "all" or arg == category:
                print("s:")
                for item in Inventory.getCurrent()[category]:
                    i = Inventory.getCurrent()[category][item]
                    print("Item ID: "+item)
                    print("Description: "+i["logoDescription"])
                    print("Price: $"+str(i["price"]))
                    print("Color: "+i["color"])
                    print("Size: "+i["size"])
                    print("In Stock: "+str(i["stockNumber"])+"\n")
        if arg == "categories":
            print("\n")
