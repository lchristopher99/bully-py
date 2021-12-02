class LoginMenu:
    # prompt user for login details and verify user with firebase
    def login():
        print("Login:")
        newUser = input("Are you a new user (y/n/exit)? ")
        if newUser == "exit":
            return 0
        if newUser == "y":
            # TODO: create new user
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
