from user.account import Account
# database
from firebase_admin import db

class LoginMenu:
    # prompt user for login details and verify user with firebase
    def login():
        login = False
        while not login:
            print("Login:")
            newUser = input("Are you a new user (y/n/exit)? ")
            if newUser == "exit":
                return 0
            if newUser == "y":
                Account.create()
            while True:
                user = input("\nUsername: ")
                pw = input("Password: ")
                if len(user) > 0 and len(pw) > 0:
                    break
                else:
                    print("\nPlease enter username/password!")
            for key in Account.getCurrent():
                if user == Account.getCurrent()[key]["username"] and pw == Account.getCurrent()[key]["password"]:
                    print("\nWelcome "+user+"!")
                    file = open("./user/login_token.txt", "w")
                    file.write(key)
                    file.close()
                    login = True
            if not login:
                print("\nUser not found in database!\n")
