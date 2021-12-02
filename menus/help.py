class HelpMenu:
    # display help menu
    def help():
        print("\n-----Available commands-----")
        print("1:     /exit               -- exits shop")
        print("2:     /loadNew            -- loads a new inventory to the bullypy database (overwrites existing data)")
        print("3:     /viewAll <category> -- view items in store with argument support.")
        print("\n       USAGE: /viewAll            - shows all items in store")
        print("              /viewAll categories - shows all categories available in store")
        print("              /viewAll hats       - shows all hats in store (this can be changed to any category)")
        print()
