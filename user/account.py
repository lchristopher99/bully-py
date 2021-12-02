import json
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
                "Total Price": 0,
                "Total Weight": 0,
                "Total Items": 0,
                "items": {

                }
            },
            "Order History": {

            }
        }

        try:
            Account.getRef().push().set(account)
            print("\nAccount created successfully!")
        except Exception as e:
            print("\nError creating user account:")
            logging.error(traceback.format_exc())
