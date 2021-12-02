from firebase import firebase
from user import *
from store_screen import store_screen
from login_screen import login_screen

db_url = "https://groupproject-8d2e6-default-rtdb.firebaseio.com/"
fb = firebase.FirebaseApplication(db_url, None)

def main():
    print("Welcome to the Bully store! Enter 'help' for a list of commands.")

    current_user = User()
    # Stay on login screen until user logs in/creates an account
    while not current_user.logged_in:
        command = input("Enter a command: ")
        if (command == "exit"):
            break
        login_screen(current_user, command)

    print("Successfully logged in. Enter 'help' for a list of commands.")
    # Stay on shopping screen until user logs out/deletes account
    while current_user.logged_in:
        command = input("Enter a command: ")
        if (command == "exit"):
            break
        store_screen(current_user, command)

    print("Goodbye!")

main()