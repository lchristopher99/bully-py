import json
import os
# database
from firebase_admin import db
# debug
import traceback
import logging

class Account:
    # returns Users json obj
    def getCurrent():
        ref = db.reference("/")
        return ref.get()["Users"]

    # returns reference to Users database
    def getRef():
        ref = db.reference("/Users")
        return ref

    # returns user key
    def getKey():
        file = open("./user/login_token.txt", "r")
        key = file.read()
        file.close()
        return key

    # removes login_token after account deletion
    def destroyKey():
        os.remove("./user/login_token.txt")

    # checks if order history is empty
    def isHistoryEmpty():
        try:
            Account.getCurrent()[Account.getKey()]["orderHistory"]
            return False
        except:
            return True

    def editAccount(infoType):
        accRef = Account.getRef().child(Account.getKey())
        if infoType == "payment":
            accRef.child("creditCard").child("name").set(input("\nUpdate card name: "))
            accRef.child("creditCard").child("number").set(input("Update card number: "))
            accRef.child("creditCard").child("expirationDate").set(input("Update expiration date: "))
            accRef.child("creditCard").child("securityCode").set(input("Update security code: "))
            print("\nPayment info updated!\n")
        elif infoType == "shipping":
            accRef.child("address").child("streetAddress").set(input("\nUpdate street address: "))
            accRef.child("address").child("state").set(input("Update state: "))
            accRef.child("address").child("city").set(input("Update city: "))
            accRef.child("address").child("zip").set(input("Update zip: "))
            print("\nShipping info updated!\n")
        elif infoType == "name":
            accRef.child("firstName").set(input("\nUpdate first name: "))
            accRef.child("lastName").set(input("Update last name: "))
            print("\nName updated!\n")
        elif infoType == "login":
            accRef.child("username").set(input("\nUpdate username: "))
            accRef.child("password").set(input("Update password: "))
            print("\nLogin updated!\n")
        else:
            print("Invalid arguments for editAccount. Format should be 'editAccount <payment/shipping/name/username>'")

    # view account details
    def viewAccount():
        accRef = Account.getCurrent()[Account.getKey()]
        print("\nFirst name: "+accRef["firstName"])
        print("Last name: "+accRef["lastName"])
        print("Username: "+accRef["username"])
        print("Password: "+accRef["password"])
        print("Payment Info:")
        print("   Card Name: "+accRef["creditCard"]["name"])
        print("   Card Number: "+str(accRef["creditCard"]["number"]))
        print("   Expiration Date: "+accRef["creditCard"]["expirationDate"])
        print("   Security Code: "+str(accRef["creditCard"]["securityCode"]))
        print("Shipping Info:")
        print("   Street Address: "+accRef["address"]["streetAddress"])
        print("   State: "+accRef["address"]["state"])
        print("   City: "+accRef["address"]["city"])
        print("   Zip: "+str(accRef["address"]["zip"])+"\n")

    # view order history
    def viewHistory():
        # if order history isnt empty
        if not Account.isHistoryEmpty():
            historyRef = Account.getCurrent()[Account.getKey()]["orderHistory"]
            for order_id in historyRef:
                i = historyRef[order_id]
                print("\nOrder "+order_id+": ")
                print("   Total Price: $"+str(i["order"]["totalPrice"]))
                print("   Total Items: "+str(i["order"]["totalItems"]))
                print("   Total Weight: "+str(i["order"]["totalWeight"])+"lbs")
                print("   Payment Info:")
                print("      Card Name: "+str(i["paymentInfo"]["name"]))
                print("      Card Number: "+str(i["paymentInfo"]["number"]))
                print("      Expiration Date: "+str(i["paymentInfo"]["expirationDate"]))
                print("      Security Code: "+str(i["paymentInfo"]["securityCode"]))
                print("   Shipping Info:")
                print("      Street Address: "+str(i["shippingInfo"]["streetAddress"]))
                print("      State: "+str(i["shippingInfo"]["state"]))
                print("      City: "+str(i["shippingInfo"]["city"]))
                print("      Zip: "+str(i["shippingInfo"]["zip"]))
                print("   Items:")
                for item_id in i["order"]["Items"]:
                    item = i["order"]["Items"][item_id]
                    print("     "+item_id+":")
                    print("     "+str(item)+"\n")
        else:
            print("\nOrder history empty!\n")

    # pushes new account json file to database
    # TODO: making this data randomized would be cool
    def loadNew():
        try:
            with open("user/account.json", "r") as f:
                file_contents = json.load(f)
            Account.getRef().push().set(file_contents)
            print("\nNew account loaded to firebase!\n")
        except Exception as e:
            print("\nError loading account file:")
            logging.error(traceback.format_exc())

    # delete current account
    def delete():
        sure = input("\nAre you sure you want to delete your account (y/n)? ")
        if sure == "y":
            accRef = Account.getRef().child(Account.getKey())
            accRef.delete()
            Account.destroyKey()
            print("\nAccount successfully deleted!\n")
            return 1
        else:
            print("\nAccount deletion aborted!\n")

    # create new account in firebase
    def create():
        firstName = input("\nEnter first name: ")
        lastName = input("Enter last name: ")
        user = input("New username: ")
        pw = input("New password: ")
        cardName = input("Enter card name: ")
        cardNum = input("Enter card number: ")
        cardExp = input("Enter card expiration date: ")
        securityCode = input("Enter card security code: ")
        addr = input("Enter address: ")
        city = input("Enter city: ")
        state = input("Enter state: ")
        zip = input("Enter zip: ")
        account = {
            "firstName": firstName,
            "lastName": lastName,
            "username": user,
            "password": pw,
            "address": {
                "streetAddress": addr,
                "city": city,
                "state": state,
                "zip": zip
            },
            "creditCard": {
                "name": cardName,
                "securityCode": securityCode,
                "expirationDate": cardExp,
                "number": cardNum
            },
            "Cart": {
                "totalItems": 0,
                "totalPrice": 0,
                "totalWeight": 0,
                "items": {

                }
            },
            "orderHistory": {

            }
        }
        try:
            Account.getRef().push().set(account)
            print("\nAccount created successfully!")
        except Exception as e:
            print("\nError creating user account:")
            logging.error(traceback.format_exc())
