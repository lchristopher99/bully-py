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
        # Check if one of the commands that has arguments has been entered
        try:
            baseCommand = ans[:ans.index(" ")]
        except:
            baseCommand = ans

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
        elif baseCommand == "/viewAll":
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
        elif baseCommand == "/addToCart":
            # Check for too few arguments and that first argument can be converted to an int
            try:
                num = ans.split(" ")[1]
                itemID = ans.split(" ")[2]

                # Check for extraneous arguments
                try:
                    test = ans.split(" ")[3]
                    tooManyArgs = True
                except:
                    tooManyArgs = False
                
                if not tooManyArgs:
                    Cart.add(int(num), itemID)
                else:
                    print("Invalid arguments for addToCart. Format should be 'addToCart <int> <item_id>'")
            except:
                print("Invalid arguments for addToCart. Format should be 'addToCart <int> <item_id>'")


        elif baseCommand == "/removeFromCart":
            # Check for too few arguments and that first argument can be converted to an int
            try:
                num = ans.split(" ")[1]
                itemID = ans.split(" ")[2]

                # Check for extraneous arguments
                try:
                    test = ans.split(" ")[3]
                    tooManyArgs = True
                except:
                    tooManyArgs = False

                if not tooManyArgs:
                    Cart.remove(int(num), itemID)
                else:
                    print("Invalid arguments for removeFromCart. Format should be 'removeFromCart <int> <item_id>'")
            except:
                print("Invalid arguments for removeFromCart. Format should be 'removeFromCart <int> <item_id>")
            
        elif ans == "/checkout":
            Cart.checkout()
        elif ans == "/viewHistory":
            Account.viewHistory()
        elif baseCommand == "/editAccount":
            # Check for too few arguments
            try:
                infoType = ans.split(" ")[1]

                # Check for extraneous arguments
                try:
                    test = ans.split(" ")[2]
                    tooManyArgs = True
                except:
                    tooManyArgs = False

                if not tooManyArgs:
                    Account.editAccount(infoType)
                else:
                    print("Invalid arguments for editAccount. Format should be 'editAccount <payment/shipping/name/username>'")
            except:
                print("Invalid arguments for editAccount. Format should be 'editAccount <payment/shipping/name/username>'")

        elif ans == "/viewAccount":
            Account.viewAccount()
        elif ans == "/deleteAccount":
            if Account.delete() == 1:
                return 1
        else:
            print("\n"+ans, "-- not a valid command. Type /help to see a list of commands.\n")
