from firebase import firebase
from requests.sessions import to_native_string

def adjust_cart(user, shirt_id, adjustment):
    fb = firebase.FirebaseApplication("https://bully-py-default-rtdb.firebaseio.com/", None)
    cart_path = "Users/" + user + "/Cart"
    cart_item_path = cart_path + "/" + shirt_id
    item_path = "Shirt/" + shirt_id

    # cartPrice += new_price
    new_price = fb.get(item_path, "price") * adjustment
    fb.put(cart_path, "cartPrice", round(fb.get(cart_path, "cartPrice") + new_price, 2))
    # cartWeight += new_weight
    new_weight = fb.get(item_path, "weight") * adjustment
    fb.put(cart_path, "cartWeight", round(fb.get(cart_path, "cartWeight") + new_weight, 2))
    # numItems += adjustment
    fb.put(cart_path, "numItems", fb.get(cart_path, "numItems") + adjustment)

    shirt = fb.get(cart_path, shirt_id)
    # Add item to cart
    if shirt == None: # Item not in cart
        # Track the total price, weight, and quantity for items in the cart
        new_item = {
            "totalItemPrice": round(new_price, 2),
            "totalItemWeight": round(new_weight, 2),
            "quantity": adjustment
        }
        # Add item information to cart
        new_item.update(fb.get(item_path, None))
        new_item.pop("stockNumber")
        name = fb.put(cart_path, shirt_id, new_item)
    # Adjust quantity, total item price, and total item weight
    else: # Item already in cart
        # Quantity += adjustment
        fb.put(cart_item_path, "quantity", fb.get(cart_item_path, "quantity") + adjustment)
        # Total item price += new_price
        fb.put(cart_item_path, "totalItemPrice", round(fb.get(cart_item_path, "Total item price") + new_price, 2))
        # Total item weight += new_weight
        fb.put(cart_item_path, "totalItemWeight", round(fb.get(cart_item_path, "Total item weight") + new_weight, 2))

    # Delete the item from the cart if its quantity has been set to 0
    if fb.get(cart_item_path, "Quantity") == 0:
        fb.delete(cart_path, shirt_id)

class Shirt:
    def add_shirt(user, shirt_id, quantity):
        fb = firebase.FirebaseApplication("https://bully-py-default-rtdb.firebaseio.com/", None)
        item_path = "Shirt/" + shirt_id

        stock = fb.get(item_path, "stockNumber")
        if (stock == None): # Shirt does not exist
            return -1
        if (stock == 0): # Shirt out of stock
            return 0

        # Add as many shirts to the cart as is available, up to the desired number
        if (stock >= quantity): # Enough items in stock
            added_shirts = quantity
            fb.put(item_path, "stockNum", stock - quantity)
        else: # Not enough items in stock
            added_shirts = stock
            fb.put(item_path, "stockNum", 0)
        adjust_cart(user, shirt_id, added_shirts)

        return added_shirts
    
    # Remove shirt from cart
    def remove_shirt(user, shirt_id, quantity):
        fb = firebase.FirebaseApplication("https://bully-py-default-rtdb.firebaseio.com/")
        item_path = "Shirt/" + shirt_id
        cart_path = "Users/" + user + "/Cart"
        cart_item_path = cart_path + "/" + shirt_id
        
        num_in_cart = fb.get(cart_item_path, "Quantity")
        if (num_in_cart == None): # Shirt not in cart
            return -1
        
        # Remove as many shirts as possible from the cart, up to the desired number
        if (num_in_cart >= quantity):
            removed_shirts = quantity
        else: 
            removed_shirts = num_in_cart
        adjust_cart(user, shirt_id, -1 * removed_shirts)
        
        # Increase the number in stock by the number of removed shirts
        fb.put(item_path, "stockNum", fb.get(item_path, "stockNum") + removed_shirts)

        return removed_shirts
