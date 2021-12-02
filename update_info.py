def update_payment(username):
    fb = firebase.FirebaseApplication("https://bully-py-default-rtdb.firebaseio.com/", None)

    new_name = input("Enter new card name: ")
    new_number = input("Enter new card number: ")
    new_code = input("Enter new security code: ")
    new_exp = input("Enter new expiration date: ")

    new_payment_info = {
        "cardName": new_name,
        "cardNumber": new_number,
        "securityCode": new_code,
        "expirationDate": new_exp
    }

    fb.put("Users/" + username, "creditCard", new_payment_info)

def update_shipping(username):
    fb = firebase.FirebaseApplication("https://bully-py-default-rtdb.firebaseio.com/", None)

    new_street = input("Enter new street address: ")
    new_city = input("Enter new city: ")
    new_state = input("Enter new state: ")
    new_zip = input("Enter new zip code: ")

    new_shipping_info = {
        "streetAddress": new_street,
        "city": new_city,
        "state": new_state,
        "zip": new_zip
    }

    fb.put("Users/" + username, "address", new_shipping_info)