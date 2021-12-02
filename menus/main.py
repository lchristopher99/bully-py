# inventory system
from inv_sys.inventory import Inventory
# menus
from menus.help import HelpMenu

class MainMenu:
    def welcomePrompt():
        print("Welcome to the BullyPy store!")
        print("-----------------------------")

    def quickHelpPrompt():
        print("Enter /help to see list of available commands or /exit to exit the shop")

    # process user commands from main loop
    def processCmd(ans):
        if ans == "/exit":
            print("Thanks for shopping with us... Goodbye :)")
            return 0
        elif ans == "/help":
            HelpMenu.help()
        elif ans == "/loadNew":
            Inventory.loadNewInventory()
        elif ans == "/viewAll":
            Inventory.viewAll("all")
        elif "/viewAll " in ans:
            # auto capitalize argument passed in
            category = ans.split(" ")[1].capitalize()
            if "categories" in ans:
                Inventory.viewAll("categories")
            # category argument can be singular/plural or uppercase/lowercase
            elif category in Inventory.getCurrentInventory():
                    Inventory.viewAll(category)
            elif category[:len(category)-1] in Inventory.getCurrentInventory():
                    Inventory.viewAll(category[:len(category)-1])
        else:
            print("\n"+ans, "-- not a valid command. Type /help to see a list of commands.\n")
