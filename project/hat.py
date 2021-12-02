from firebase import firebase

db_url = "https://groupproject-8d2e6-default-rtdb.firebaseio.com/"

def adjust_cart(user, item_id, adjustment):
    fb = firebase.FirebaseApplication(db_url, None)
    cart_path = "Users/" + user + "/Cart"
    cart_item_path = cart_path + "/" + item_id
    item_path = "Hat/" + item_id

    new_price = fb.get(item_path, "price") * adjustment
    fb.put(cart_path, "cartPrice", round(fb.get(cart_path, "cartPrice") + new_price, 2))
    new_weight = fb.get(item_path, "weight") * adjustment
    fb.put(cart_path, "cartWeight", round(fb.get(cart_path, "cartWeight") + new_weight, 2))
    fb.put(cart_path, "numItems", fb.get(cart_path, "numItems") + adjustment)

    item = fb.get(cart_path, item_id)
    if item == None:
        new_item = {
            "totalItemPrice": round(new_price, 2),
            "totalItemWeight": round(new_weight, 2),
            "quantity": adjustment
        }
        new_item.update(fb.get(item_path, None))
        new_item.pop("stockNumber")
        name = fb.put(cart_path, item_id, new_item)
    else:
        fb.put(cart_item_path, "quantity", fb.get(cart_item_path, "quantity") + adjustment)
        fb.put(cart_item_path, "totalItemPrice", round(fb.get(cart_item_path, "totalItemPrice") + new_price, 2))
        fb.put(cart_item_path, "totalItemWeight", round(fb.get(cart_item_path, "totalItemWeight") + new_weight, 2))

    if fb.get(cart_item_path, "Quantity") == 0:
        fb.delete(cart_path, item_id)

class Hat:
    def add_item(self, user, item_id, quantity):
        fb = firebase.FirebaseApplication(db_url, None)
        item_path = "Hat/" + item_id

        stock = fb.get(item_path, "stockNumber")
        if (stock == None):
            return -1
        if (stock == 0):
            return 0

        if (stock >= quantity):
            added_items = quantity
            fb.put(item_path, "stockNumber", stock - quantity)
        else:
            added_items = stock
            fb.put(item_path, "stockNumber", 0)
        adjust_cart(user, item_id, added_items)

        return added_items
    
    def remove_item(self, user, item_id, quantity):
        fb = firebase.FirebaseApplication(db_url, None)
        item_path = "Hat/" + item_id
        cart_path = "Users/" + user + "/Cart"
        cart_item_path = cart_path + "/" + item_id
        
        num_in_cart = fb.get(cart_item_path, "quantity")
        if (num_in_cart == None):
            return -1
        if (num_in_cart >= quantity):
            removed_items = quantity
        else: 
            removed_items = num_in_cart
        adjust_cart(user, item_id, -1 * removed_items)
        
        fb.put(item_path, "stockNumber", fb.get(item_path, "stockNumber") + removed_items)

        return removed_items

    def display(self):
        fb = firebase.FirebaseApplication(db_url, None)
        category_path = "Hat/"

        items = fb.get(category_path, None)
        for key, value in items.items():
            print(key, value)