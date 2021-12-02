# menus
from menus.main import MainMenu
from menus.login import LoginMenu
# database
from db.firebase import Firebase

def main():
    # initialize database
    Firebase.init_rtdb()

    MainMenu.welcomePrompt()
    if LoginMenu.login() == 0:
        return 0
    MainMenu.quickHelpPrompt()

    # main loop
    while True:
        cmd = MainMenu.processCmd(input("$ "))
        if cmd == 1:
            if LoginMenu.login() == 0:
                return 0
            MainMenu.quickHelpPrompt()
        elif cmd == 0:
            return 0

main()
