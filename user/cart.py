import json
# database
from firebase_admin import db
# debug
import traceback
import logging

class Cart:
    # returns Cart json obj
    def getCurrent():
        ref = db.reference("/")
        file = open("./user/login_token.txt", "r")
        key = file.read()
        file.close()
        return ref.get()["Users"][key]["Cart"]

    # returns db reference to user cart
    def getRef():
        file = open("./user/login_token.txt", "r")
        key = file.read()
        file.close()
        ref = db.reference("/Users")[key]["Cart"]
        return ref

    # view all items in cart
    def viewCart():
        print("\nTotal Price: "+str(Cart.getCurrent()["totalPrice"]))
        print("Total Items: "+str(Cart.getCurrent()["totalItems"]))
        print("Total Weight: "+str(Cart.getCurrent()["totalWeight"]))
        try:
            for item in Cart.getCurrent()["Items"]:
                print(item)
        except:
            print("No items in your cart!\n")
