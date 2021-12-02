# menus
from menus.main import MainMenu
from menus.login import LoginMenu
# database
from db.firebase import Firebase

def main():
    # initialize database
    Firebase.init_db()

    MainMenu.welcomePrompt()
    if LoginMenu.login() == 0:
        return 0
    MainMenu.quickHelpPrompt()

    # main loop
    while True:
        if MainMenu.processCmd(input("$ ")) == 0:
            return 0

main()
