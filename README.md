# Atm-management

# libraries to install
    pip install pymongo
    pip install colorama


#Important:

Add your connection string.

Add your email.

Add your gmail password (Google account setting) > Security > (Make sure 2-step verification is on.) > App passwords.

A user cannot be created before Admin

A minimum of five user registrations is allowed.

Deposit limit: $100,000.

Withdrawal limit: $50,000.

Admin deposit limit: 300k

If a user enters an incorrect password, the account will be locked for 10 minutes.

Only the administrator can delete, lock, show all accounts, or unlock the user account.

If the total balance of the user and admin is below 75k, then it will print a message saying the balance is below 75k.

A timeout function. If the user doesn't enter any input for 30 seconds, then the program will exit.Implemented on Login and change password panel (can be implemented on other panel too)


Menu contains:-
1. User panel
    1. Register user
    2. User login
        1. Deposit Money
        2. Withdraw Money
        3. Check Balance
        4. Change Password
        5. Exit
    3. Exit
2. Admin panel
    1. Register Admin
    2. Admin login
        1. Lock or unlock the user account
        2.  Delete the user account
        3.  Check the total balance.
        4.  Change Password for Admin Account
        5.  Change Password for user
        6.  Show all the user accounts
        7.  Deposit
        8.  Exit
    3.Exit
3. Exit 
