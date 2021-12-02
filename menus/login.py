from user.userAccount import UserAccount

class LoginMenu:
    # prompt user for login details and verify user with firebase
    def login():
        print("Login:")
        newUser = input("Are you a new user (y/n/exit)? ")
        if newUser == "exit":
            return 0
        if newUser == "y":
            firstName = input("\nEnter first name: ")
            lastName = input("Enter last name: ")
            user = input("New username: ")
            pw = input("New password: ")
            cardName = input("Enter card name: ")
            cardNum = input("Enter card number: ")
            cardExp = input("Enter card expiration date: ")
            cardCVV = input("Enter card security code: ")
            addr = input("Enter address: ")
            city = input("Enter city: ")
            state = input("Enter state: ")
            zip = input("Enter zip: ")
            newAcc = UserAccount(
                firstName,
                lastName,
                user,
                pw,
                cardName,
                cardNum,
                cardExp,
                cardCVV,
                addr,
                city,
                state,
                zip
            )
            print("\nNew account created!")
        while True:
            user = input("\nUsername: ")
            pw = input("Password: ")
            if len(user) > 0 and len(pw) > 0:
                break
            else:
                print("\nPlease enter username/password!")
        # TODO: verify user login
        print("\nWelcome "+user+"!")
