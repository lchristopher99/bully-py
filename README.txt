Before running bully.py make sure firebase_admin is installed on your machine

  1. pip install firebase_admin
  2. python3 bully.py

  NOTE: There is no checking for unique usernames,
        so if /loadNew is ran multiple times, either
        comment out Account.loadNew() on line 25
        of main.py, or edit newly pushed account login info
        so when logging in, you're routed to the correct account.
        This also goes for accounts created thru signup process.
        If an account is created with the same user and pass,
        a unique key will be generated for that user, but there is no guarantee
        you'll be routed to the correct account after login
  NOTE: Default login after /loadNew is:
        user: b_lazar
        pass: 123

test
