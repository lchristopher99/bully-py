import json
from inv_sys.inventory import Inventory
from user.account import Account
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
        ref = db.reference("/Users").child(key).child("Cart")
        return ref

    # checkout items in cart
    def checkout():
        exist = False
        # if cart is not empty
        if not Cart.isEmpty():
            # for each item in cart
            for item_id in Cart.getCurrent()["Items"]:
                    # loop thru inventory to find matching item
                    for category in Inventory.getCurrent():
                        for itemID in Inventory.getCurrent()[category]:
                            if itemID == item_id:
                                exist = True
                                invObj = Inventory.getCurrent()[category][itemID]
                                invRef = Inventory.getRef().child(category).child(itemID)
                                cartObj = Cart.getCurrent()["Items"][item_id]
                                # if last in stock, remove from db
                                if invObj["stockNumber"] == 1:
                                    invRef.delete()
                                # else, decrement stock number
                                else:
                                    dec = invObj["stockNumber"] - cartObj["stockNumber"]
                                    invRef.child("stockNumber").set(dec)
        else:
            print("\nCart empty, nothing to checkout!\n")
        if exist:
            key = Account.getKey()
            accRef = Account.getRef().child(key)
            accObj = Account.getCurrent()[key]
            cartRef = Cart.getRef()
            order = {
                "order": Cart.getCurrent(),
                "paymentInfo": accObj["creditCard"],
                "shippingInfo": accObj["address"]
            }
            # add order to history
            accRef.child("orderHistory").push().set(order)
            # clear cart
            cartRef.child("Items").delete()
            # reset cart total values
            cartRef.child("totalItems").set(0)
            cartRef.child("totalPrice").set(0)
            cartRef.child("totalWeight").set(0)
            print("\nCheckout successful! View order history for details...\n")

    # add num items to cart
    def add(num, itemID):
        try:
            i = 0
            print()
            while i < num:
                itemObj = None
                exist = False
                max = False
                for category in Inventory.getCurrent():
                    for item_id in Inventory.getCurrent()[category]:
                        if itemID == item_id:
                            itemObj = Inventory.getCurrent()[category][itemID]
                            itemRef = Inventory.getRef().child(category).child(itemID)
                            cartRef = Cart.getRef().child("Items")
                            # if cart is not empty
                            if not Cart.isEmpty():
                                # if item already in cart, increment cart number
                                for cart_item_id in Cart.getCurrent()["Items"]:
                                    if itemID == cart_item_id:
                                        exist = True
                                        cartObj = Cart.getCurrent()["Items"][itemID]
                                        # if cart number exceeds inventory number, prompt user
                                        if cartObj["stockNumber"] == itemObj["stockNumber"]:
                                            max = True
                                            print("Max stock reached for item!")
                                        else:
                                            inc = cartObj["stockNumber"] + 1
                                            cartRef.child(itemID).child("stockNumber").set(inc)
                            # if item does not already exist in cart, push to cart
                            if not exist:
                                exist = True
                                # send obj to cart with key being itemID
                                cartRef.child(itemID).set(itemObj)
                                # set stock number to 1 for new item
                                cartRef.child(itemID).child("stockNumber").set(1)
                if exist:
                    if not max:
                        # increment total items
                        inc = Cart.getCurrent()["totalItems"] + 1
                        Cart.getRef().child("totalItems").set(inc)
                        # calculate price
                        newTotal = Cart.getCurrent()["totalPrice"] + itemObj["price"]
                        Cart.getRef().child("totalPrice").set(round(newTotal, 2))
                        # calculate weight
                        newWeight = Cart.getCurrent()["totalWeight"] + itemObj["weight"]
                        Cart.getRef().child("totalWeight").set(round(newWeight, 2))
                        # if max stock hasnt been reached on an item
                        if not max and i == 0:
                            print(itemObj)
                        print("Item added to cart!")
                else:
                    print(itemID+" -- item not found in inventory!")
                i += 1
            print()
        except Exception as e:
            print("\nError adding item to cart:")
            logging.error(traceback.format_exc())

    # remove num items from cart
    def remove(num, itemID):
        try:
            i = 0
            print()
            while i < num:
                itemObj = None
                exist = False
                # if cart is not empty
                if not Cart.isEmpty():
                    for item_id in Cart.getCurrent()["Items"]:
                        if itemID == item_id:
                            exist = True
                            itemObj = Cart.getCurrent()["Items"][itemID]
                            itemRef = Cart.getRef().child("Items").child(itemID)
                            # get category from first name in itemID
                            invRef = Inventory.getRef().child(itemID.split("_")[0].capitalize())
                            # if last in cart, remove from db
                            if itemObj["stockNumber"] == 1:
                                itemRef.delete()
                            # else, decrement cart number
                            else:
                                dec = itemObj["stockNumber"] - 1
                                itemRef.child("stockNumber").set(dec)
                    if exist:
                        # decrement total items
                        dec = Cart.getCurrent()["totalItems"] - 1
                        Cart.getRef().child("totalItems").set(dec)
                        # calculate price
                        if Cart.getCurrent()["totalItems"] == 0:
                            Cart.getRef().child("totalPrice").set(0)
                        else:
                            newTotal = Cart.getCurrent()["totalPrice"] - itemObj["price"]
                            Cart.getRef().child("totalPrice").set(round(newTotal, 2))
                        # calculate weight
                        newWeight = Cart.getCurrent()["totalWeight"] - itemObj["weight"]
                        Cart.getRef().child("totalWeight").set(round(newWeight, 2))
                        if i == 0:
                            print(itemObj)
                        print("Item removed from cart!")
                    else:
                        print(itemID+" -- item not found in cart!")
                else:
                    print("Cart is empty!")
                i += 1
            print()
        except Exception as e:
            print("\nError removing item from cart:")
            logging.error(traceback.format_exc())

    # checks if cart is empty
    def isEmpty():
        try:
            Cart.getCurrent()["Items"]
            return False
        except:
            return True

    # view all items in cart
    def viewCart():
        try:
            for item in Cart.getCurrent()["Items"]:
                i = Cart.getCurrent()["Items"][item]
                print("\nItem ID: "+item)
                print("Description: "+i["logoDescription"])
                print("Price: $"+str(i["price"]))
                print("Color: "+i["color"])
                print("Size: "+i["size"])
                print("In Cart: "+str(i["stockNumber"]))

            print("\nTotal Price: $"+str(Cart.getCurrent()["totalPrice"]))
            print("Total Items: "+str(Cart.getCurrent()["totalItems"]))
            print("Total Weight: "+str(Cart.getCurrent()["totalWeight"])+"lbs\n")
        except:
            print("\nNo items in your cart!\n")
