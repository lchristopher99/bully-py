from firebase import firebase

db_url = "https://groupproject-8d2e6-default-rtdb.firebaseio.com/"

def adjust_cart(user, item_id, adjustment):
    fb = firebase.FirebaseApplication(db_url, None)
    cart_path = "Users/" + user + "/Cart"
    cart_item_path = cart_path + "/" + item_id
    item_path = "Shirt/" + item_id

    # cartPrice += new_price
    new_price = fb.get(item_path, "price") * adjustment
    fb.put(cart_path, "cartPrice", round(fb.get(cart_path, "cartPrice") + new_price, 2))
    # cartWeight += new_weight
    new_weight = fb.get(item_path, "weight") * adjustment
    fb.put(cart_path, "cartWeight", round(fb.get(cart_path, "cartWeight") + new_weight, 2))
    # numItems += adjustment
    fb.put(cart_path, "numItems", fb.get(cart_path, "numItems") + adjustment)

    item = fb.get(cart_path, item_id)
    # Add item to cart
    if item == None: # Item not in cart
        # Track the total price, weight, and quantity for items in the cart
        new_item = {
            "totalItemPrice": round(new_price, 2),
            "totalItemWeight": round(new_weight, 2),
            "quantity": adjustment
        }
        # Add item information to cart
        new_item.update(fb.get(item_path, None))
        new_item.pop("stockNumber")
        name = fb.put(cart_path, item_id, new_item)
    # Adjust quantity, total item price, and total item weight
    else: # Item already in cart
        # quantity += adjustment
        fb.put(cart_item_path, "quantity", fb.get(cart_item_path, "quantity") + adjustment)
        # Total item price += new_price
        fb.put(cart_item_path, "totalItemPrice", round(fb.get(cart_item_path, "totalItemPrice") + new_price, 2))
        # Total item weight += new_weight
        fb.put(cart_item_path, "totalItemWeight", round(fb.get(cart_item_path, "totalItemWeight") + new_weight, 2))

    # Delete the item from the cart if its quantity has been set to 0
    if fb.get(cart_item_path, "quantity") == 0:
        fb.delete(cart_path, item_id)

class Shirt:
    def add_item(self, user, item_id, quantity):
        fb = firebase.FirebaseApplication(db_url, None)
        item_path = "Shirt/" + item_id

        stock = fb.get(item_path, "stockNumber")
        if (stock == None): # Shirt does not exist
            return -1
        if (stock == 0): # Shirt out of stock
            return 0

        # Add as many shirts to the cart as is available, up to the desired number
        if (stock >= quantity): # Enough items in stock
            added_items = quantity
            fb.put(item_path, "stockNumber", stock - quantity)
        else: # Not enough items in stock
            added_items = stock
            fb.put(item_path, "stockNumber", 0)
        adjust_cart(user, item_id, added_items)

        return added_items
    
    # Remove shirt from cart
    def remove_item(self, user, item_id, quantity):
        fb = firebase.FirebaseApplication(db_url, None)
        item_path = "Shirt/" + item_id
        cart_path = "Users/" + user + "/Cart"
        cart_item_path = cart_path + "/" + item_id
        
        num_in_cart = fb.get(cart_item_path, "quantity")
        if (num_in_cart == None): # Shirt not in cart
            return -1
        # Remove as many shirts as possible from the cart, up to the desired number
        if (num_in_cart >= quantity):
            removed_items = quantity
        else: 
            removed_items = num_in_cart
        adjust_cart(user, item_id, -1 * removed_items)
        
        # Increase the number in stock by the number of removed shirts
        fb.put(item_path, "stockNumber", fb.get(item_path, "stockNumber") + removed_items)

        return removed_items

    def display(self):
        fb = firebase.FirebaseApplication(db_url, None)
        category_path = "Shirt/"

        items = fb.get(category_path, None)
        for key, value in items.items():
            print(key, value)