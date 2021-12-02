# inventory system
from inv_sys.inventory import Inventory
from user.account import Account
from user.cart import Cart
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
            HelpMenu.display()
        elif ans == "/loadNew":
            Inventory.loadNew()
            Account.loadNew()
        elif ans == "/viewAll":
            Inventory.viewAll("all")
        elif "/viewAll " in ans:
            # auto capitalize argument passed in
            category = ans.split(" ")[1].capitalize()
            if "categories" in ans:
                Inventory.viewAll("categories")
            # category argument can be singular/plural or uppercase/lowercase
            elif category in Inventory.getCurrent():
                    Inventory.viewAll(category)
            elif category[:len(category)-1] in Inventory.getCurrent():
                    Inventory.viewAll(category[:len(category)-1])
        elif ans == "/viewCart":
            Cart.viewCart()
        elif "/addToCart " in ans:
            num = ans.split(" ")[1]
            itemID = ans.split(" ")[2]
            Cart.add(int(num), itemID)
        elif "/removeFromCart " in ans:
            num = ans.split(" ")[1]
            itemID = ans.split(" ")[2]
            Cart.remove(int(num), itemID)
        elif ans == "/checkout":
            Cart.checkout()
        elif ans == "/viewHistory":
            Account.viewHistory()
        elif "/editAccount " in ans:
            infoType = ans.split(" ")[1]
            Account.editAccount(infoType)
        elif ans == "/viewAccount":
            Account.viewAccount()
        elif ans == "/deleteAccount":
            if Account.delete() == 1:
                return 1
        else:
            print("\n"+ans, "-- not a valid command. Type /help to see a list of commands.\n")
