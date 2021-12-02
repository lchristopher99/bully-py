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
            "First Name": firstName,
            "Last Name": lastName,
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
                "cartPrice": 0,
                "cartWeight": 0,
                "numItems": 0
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
