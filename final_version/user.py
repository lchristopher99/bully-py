from firebase import firebase
from shirt import Shirt
from jacket import Jacket
from hat import Hat
from cowbell import Cowbell

db_url = "https://groupproject-8d2e6-default-rtdb.firebaseio.com/"
fb = firebase.FirebaseApplication(db_url, None)

class User:
    def __init__(self):
        self.username = "" # Used to get path to user in database
        self.logged_in = False

    def edit_shipping(self, street_address, city, state, zip):
        new_address = {
            "street": street_address,
            "city": city,
            "state": state,
            "zip": zip
        }
        fb.put("Users/" + self.username, "shipping", new_address)
    
    def edit_payment(self, card_number, card_name, card_security, card_expiration):
        new_payment = {
            "name": card_name,
            "number": card_number,
            "security": card_security,
            "expiration": card_expiration
        }
        fb.put("Users/" + self.username, "payment", new_payment)
    
    def add_to_cart(self, item_id, quantity):
        # Determine the item category
        try:
            underscore_index = item_id.index("_")
            category = item_id[:underscore_index]
        except:
            return -1
        
        if category == "shirt":
            item = Shirt()
        elif category == "hat":
            item = Hat()
        elif category == "jacket":
            item = Jacket()
        elif category == "cowbell":
            item = Cowbell()
        else:
            return -1
        
        added_items = item.add_item(self.username, item_id, quantity)
        return added_items

    def remove_from_cart(self, item_id, quantity):
        # Determine the item category
        try:
            underscore_index = item_id.index("_")
            category = item_id[:underscore_index]
        except:
            return -1

        if category == "shirt":
            item = Shirt()
        elif category == "hat":
            item = Hat()
        elif category == "jacket":
            item = Jacket()
        elif category == "cowbell":
            item = Cowbell()
        else:
            return -1

        removed_items = item.remove_item(self.username, item_id, quantity)
        return removed_items
    
    def checkout(self):
        # Check if cart is empty (cart always includes info on total price, total items, and total weight)
        cart = fb.get("Users/" + self.username, "Cart")
        if len(cart) < 4:
            return -1

        # Copy cart information to order history
        order_history = fb.get("Users/" + self.username, "orderHistory")
        try:
            num_orders = len(order_history)
        except: # No orders placed
            num_orders = 0
        order_num = "order" + str(num_orders + 1)
        fb.put("Users/" + self.username + "/orderHistory", order_num, cart)
        # Copy payment and shipping
        payment = fb.get("Users/" + self.username, "payment")
        shipping = fb.get("Users/" + self.username, "shipping")
        fb.put("Users/" + self.username + "/orderHistory/" + order_num, "payment", payment)
        fb.put("Users/" + self.username + "/orderHistory/" + order_num, "shipping", shipping)

        # Clear cart
        fb.delete("Users/" + self.username, "Cart")
        new_cart = {
            "cartPrice": 0,
            "cartWeight": 0,
            "numItems": 0
        }
        fb.put("Users/" + self.username, "Cart", new_cart)

        return 0

    def display_orders(self):
        # Check if any orders have been placed
        order_history = fb.get("Users/" + self.username, "orderHistory")
        if order_history == None: # No orders
            return -1
        print(order_history)
    
    def display_cart(self):
        cart = fb.get("Users/" + self.username, "Cart")
        if len(cart) < 4: # Empty cart
            return -1
        print(cart)

    # Clear cart, restock inventory
    def clear_cart(self):
        cart = fb.get("Users/" + self.username, "Cart")
        for item in cart.items():
            try: # If item_id
                # Get num in cart
                quantity = fb.get("Users/" + self.username + "/Cart/" + item[0], "quantity")
                # Restock by num in cart
                category = item[0][:item[0].index("_")]
                if category == "shirt":
                    old_stock = fb.get("Shirt/" + item[0], "stockNumber")
                    fb.put("Shirt/" + item[0], "stockNumber", old_stock + quantity)
                elif category == "hat":
                    old_stock = fb.get("Hat/" + item[0], "stockNumber")
                    fb.put("Shirt/" + item[0], "stockNumber", old_stock + quantity)
                elif category == "jacket":
                    old_stock = fb.get("Jacket/" + item[0], "stockNumber")
                    fb.put("Shirt/" + item[0], "stockNumber", old_stock + quantity)
                elif category == "cowbell":
                    old_stock = fb.get("Cowbell/" + item[0], "stockNumber")
                    fb.put("Shirt/" + item[0], "stockNumber", old_stock + quantity)
            except:
                pass
        