import pymongo
import sys 
# library for time 
import time
from time import sleep
# library for getting unique number 
import uuid
import os
# libraries for sending maik
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



# Connect to MongoDB Atlas. please replace this with your own
client = pymongo.MongoClient("mongodb+srv://atulkumar86281:Passwordatlas1@cluster0.du9k7ti.mongodb.net/?retryWrites=true&w=majority")
# Database name
db = client["Atm_management"]

# Create user and admin collection
user_collection = db["users"]
admin_collection = db["admin"]

try:
    client.admin.command('ping')
    print(" You have successfully connected to your MongoDB!")
except Exception as e:
    print(e)



# Add a new field to the user and admin documents to track login attempts and lock status. Not needed
# user_collection.update_many({}, {"$set": {"login_attempts": 0, "account_locked": False}})
# admin_collection.update_many({}, {"$set": {"login_attempts": 0, "account_locked": False}})

# Define the number of allowed login attempts and lock duration
MAX_LOGIN_ATTEMPTS = 3
LOCK_DURATION_SECONDS = 600  # 10 minutes





#Function for Sending emails

def send_email(subject, message, to_email):
    from_email = "atul81595@gmail.com"
    app_password = "bcjm azmj hssv doit"  # generate from app password option in two step verification

    msg = MIMEMultipart()
    msg['From'] = from_email 
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, app_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")

# clear screen function 
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# function to count the number of objects present in the collection 
def countNumber(value):
    count = value.count_documents({})
    return count


# function for user login 

def Userlogin():
    count = user_collection.count_documents({})
    if count == 0:
        print(" ______________________________________________________________")
        print("|                                                              |")
        print("|                 NO USER IS REGISTERED                        |")
        print("|                                                              |")
        print(" --------------------------------------------------------------")
        sys.exit()
    user_id = input("Please enter your user_id: ")
    password = input("Please enter your user password: ")
    clear_screen()

    # Search for the user by user_id
    user = user_collection.find_one({"user_id": user_id})

    if user:
        if not user["account_locked"] :
            stored_password = user["password"]
            if password == stored_password:
                print("  ______________________________________________________________")
                print(" |                                                              |")
                print(f" |         Login successful. Welcome,  {user['name']}                      |")
                print(" |                                                              |")
                print("  --------------------------------------------------------------")
                sleep(2)
                clear_screen()
                # Reset login attempts on successful login
                user_collection.update_one({"user_id": user_id}, {"$set": {"login_attempts": 0,"account_locked": False,"lock_time":0}})
                while True:
                    print(" __________________________________________________")
                    print("|                                                  |")
                    print("|               1. DEPOSIT MONEY                   |")
                    print("|                                                  |")
                    print("|               2. WITHDRAW MONEY                  |")
                    print("|                                                  |")
                    print("|               3. CHECK BALANCE                   |")
                    print("|                                                  |")
                    print("|               4. CHANGE PASSWORD                 |")
                    print("|                                                  |")
                    print("|               5. EXIT                            |")
                    print("|                                                  |")
                    print("|             PLEASE CHOOSE YOUR OPTION            |")
                    print(" --------------------------------------------------")
                    choiceT = int(input("Enter: "))
                    sleep(1)
                    clear_screen()
                    print("")
                    if choiceT == 1:
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|       PLEASE ENTER THE AMOUNT YOU WANT TO DEPOSIT            |")
                        print("|                                                              |")
                        print("|                DEPOSIT LIMIT IS 100K                         |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
                        amountD = int(input("Enter: "))
                        clear_screen()
                        if amountD <= 100000:
                            user_collection.update_one({"user_id": user_id}, {"$inc": {"balance":amountD}})
                            print("")
                            print(" ______________________________________________________________")
                            print("|                                                              |")
                            print("|                 AMOUNT DEPOSITED SUCCESSFULLY                |")
                            print("|                                                              |")
                            print(" --------------------------------------------------------------")
                            user = user_collection.find_one({"user_id": user_id})
                            subject = "Money Credited"
                            message = f"Your account is credited by INR {amountD}. ACC balance is {user['balance']} "
                            to_email = user["gmail"]  # Replace with the user's email
                            send_email(subject, message, to_email)
                            sys.exit()
                            break
                        else:
                            print(" ______________________________________________________________")
                            print("|                                                              |")
                            print("|                 PLEASE ENTER WITHIN LIMIT                    |")
                            print("|                                                              |")
                            print(" --------------------------------------------------------------")
                    elif choiceT == 2:
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|       PLEASE ENTER THE AMOUNT YOU WANT TO WITHDRAW           |")
                        print("|                                                              |")
                        print("|                WITHDRAW LIMIT IS 50K                         |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
                        withdraw = int(input("Enter: "))
                        if withdraw <= 50000:
                            user_collection.update_one({"user_id": user_id}, {"$inc": {"balance":-withdraw}})
                            print(" ______________________________________________________________")
                            print("|                                                              |")
                            print("|                 MONEY WITHDRAWN SUCCESSFULLY                 |")
                            print("|                                                              |")
                            print(" --------------------------------------------------------------")
                            user = user_collection.find_one({"user_id": user_id})
                            subject = "Money Debited"
                            message = f"Your account is Debited by INR {withdraw}. ACC balance is {user['balance']} "
                            to_email = user["gmail"]  # Replace with the user's email
                            send_email(subject, message, to_email)
                            sys.exit()
                        else:
                            print(" ______________________________________________________________")
                            print("|                                                              |")
                            print("|                 PLEASE ENTER WITHIN LIMIT                    |")
                            print("|                                                              |")
                            print(" --------------------------------------------------------------")
                            break
                    elif choiceT == 3:
                        # clear_screen()
                        print("")
                        user = user_collection.find_one({"user_id": user_id})
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|                   SHOWING USER BALANCE                       |")
                        print("|                                                              |")
                        print(f"|                 User_id = {user['user_id']}                            |")
                        print("|                                                              |")
                        print(f"|                 Balance = {user['balance']}                                |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
                        input("Press enter to continue: ")
                        clear_screen()

                    elif choiceT == 4:
                        print(f"Enter the new Password for {user['user_id']}")
                        new_pass = input("Enter: ")
                        clear_screen()
                        user_collection.update_one({"user_id": user_id}, {"$set": {"password":new_pass}})
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|                 PASSWORD UPDATED SUCCESSFULLY                |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
                        subject = "Password Changed"
                        message = f"Your account Password has been changed "
                        to_email = user["gmail"]  # Replace with the user's email
                        send_email(subject, message, to_email)
                        sys.exit()
                    elif choiceT == 5:
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|                    EXITING USER DASHBOARD                    |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
                        sys.exit()
                    else:
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|                 PLEASE ENTER A VALID CHOICE                  |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
                
            else:
                
                print(" ______________________________________________________________")
                print("|                                                              |")
                print("|             Incorrect password. Login failed.                |")
                print("|                                                              |")
                print(" --------------------------------------------------------------")
                # Update login attempts and lock the account if needed
                user_collection.update_one({"user_id": user_id}, {"$inc": {"login_attempts": 1}})
                login_attempts = user_collection.find_one({"user_id": user_id})["login_attempts"]
                if login_attempts >= MAX_LOGIN_ATTEMPTS:
                    print("  __________________________________________________________________________________________________")
                    print(" |                                                                                                  |")
                    print(f" |  Account locked for {LOCK_DURATION_SECONDS // 60} minutes due to too many failed login attempts. |")
                    print(" |                                                                                                  |")
                    print("  --------------------------------------------------------------------------------------------------")
                    user_collection.update_one({"user_id": user_id}, {"$set": {"account_locked": True, "lock_time": int(time.time())}})
                    user = user_collection.find_one({"user_id": user_id})
                    subject = "Account locked"
                    message = f"Your account has been locked for 10 minutes. Due to too many failed login attempts.Try to login later"
                    to_email = user["gmail"]  # Replace with the user's email
                    send_email(subject, message, to_email)
        else:
            lock_time = user["lock_time"]
            current_time = int(time.time())
            if current_time - lock_time >= LOCK_DURATION_SECONDS:
                # Unlock the account if the lock duration has passed
                user_collection.update_one({"user_id": user_id}, {"$set": {"account_locked": False,"lock_time":0,"login_attempts": 0}})
                print(" ______________________________________________________________")
                print("|                                                              |")
                print("|     Account unlocked. You may attempt to login Now           |")
                print("|                                                              |")
                print(" --------------------------------------------------------------")
            else:
                remaining_lock_time = LOCK_DURATION_SECONDS - (current_time - lock_time)
                print("  ________________________________________________________________________")
                print(" |                                                                        |")
                print(f" | Account is locked. Try again after {remaining_lock_time // 60} minutes                           |")
                print(" |                                                                        |")
                print("  -------------------------------------------------------------------------")
    else:
        print(" ______________________________________________________________")
        print("|                                                              |")
        print("|         User not found. Please check your user_id            |")
        print("|                                                              |")
        print(" --------------------------------------------------------------")

# function for admin login 

def adminLogin():
    count = admin_collection.count_documents({})
    if count == 0:
        print(" ______________________________________________________________")
        print("|                                                              |")
        print("|                NO ADMIN IS REGISTERED                        |")
        print("|                                                              |")
        print(" --------------------------------------------------------------")
        sys.exit()
    admin_id = input("Please enter your admin_id: ")
    password = input("Please enter your admin password: ")

    # Search for the admin by admin_id
    admin = admin_collection.find_one({"admin_id": admin_id})

    if admin:
        if  not admin["account_locked"]:
            stored_password = admin["password"]
            if password == stored_password:
                print("  _____________________________________________________________")
                print(" |                                                              |")
                print(f" |         Login successful. Welcome,  {admin['name']}                     |")
                print(" |                                                              |")
                print("  --------------------------------------------------------------")
                sleep(2)
                clear_screen()
                print("")
                # Reset login attempts on successful login
                admin_collection.update_one({"admin_id": admin_id}, {"$set": {"login_attempts": 0,"account_locked": False,"lock_time":0}})
                while True:
                    print(" __________________________________________________")
                    print("|                                                  |")
                    print("|               1. LOCK/UNLOCK USER ACC            |")
                    print("|                                                  |")
                    print("|               2. DELETE USER ACC                 |")
                    print("|                                                  |")
                    print("|               3. CHECK BALANCE                   |")
                    print("|                                                  |")
                    print("|               4. CHANGE PASSWORD                 |")
                    print("|                                                  |")
                    print("|               5. EXIT                            |")
                    print("|                                                  |")
                    print("|             PLEASE CHOOSE YOUR OPTION            |")
                    print(" --------------------------------------------------")
                    choiceT = int(input("Enter: "))
                    clear_screen()
                    if choiceT == 1:
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|      PLEASE ENTER THE ACC ID YOU WANT TO LOCK\\UNLOCK        |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
                        acc = input("Enter: ")
                        clear_screen()
                        user = user_collection.find_one({"user_id": acc})
                        print(" ______________________________________________________________________")
                        print("|                                                                      |")
                        print("|     If you want to Lock user, press 'L'. To Unlock, press 'U':       |")
                        print("|                                                                      |")
                        print("|                     PLEASE CHOOSE YOUR OPTION                        |")
                        print(" ---------------------------------------------------------------------")
                        option = input("Enter: ")
                        clear_screen()
                        if user and option.upper() == 'L':
                            user_collection.update_one({"user_id": acc}, {"$set": {"account_locked":True,"lock_time": int(time.time())}})
                            print("")
                            print(" ______________________________________________________________")
                            print("|                                                              |")
                            print("|                 AMOUNT LOCKED SUCCESSFULLY                   |")
                            print("|                                                              |")
                            print(" --------------------------------------------------------------")
                            # admin = admin_collection.find_one({"admin_id": admin_id})
                            # subject = "Money Credited"
                            # message = f"Your Admin account is credited by INR {amountD}. ACC balance is {admin['balance']} "
                            # to_email = admin["gmail"]  # Replace with the user's email
                            # send_email(subject, message, to_email)
                            sys.exit()
                            break
                        elif user and option.upper() == 'U':
                            user_collection.update_one({"user_id": acc}, {"$set": {"account_locked":False,"lock_time":0}})
                            print("")
                            print(" ______________________________________________________________")
                            print("|                                                              |")
                            print("|                 AMOUNT UNLOCKED SUCCESSFULLY                 |")
                            print("|                                                              |")
                            print(" --------------------------------------------------------------")
                        else:
                            print(" ______________________________________________________________")
                            print("|                                                              |")
                            print("|                 PLEASE ENTER CORRECT USER ID                 |")
                            print("|                                                              |")
                            print(" --------------------------------------------------------------")
                    elif choiceT == 2:
                        print("Are you sure you want to Delete?. You cannot Redo this Action!")
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|         PLEASE ENTER THE ACC ID YOU WANT TO DELETE           |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")

                        user_to_delete = input("Enter the user ID you want to delete: ")

                        # Perform the delete operation
                        result = user_collection.delete_one({"user_id": user_to_delete})

                        # Check if the delete operation was successful
                        if result.deleted_count == 1:
                            print(" ______________________________________________________________")
                            print("|                                                              |")
                            print(f"|  User with user ID {user_to_delete} has been deleted                   |")
                            print("|                                                              |")
                            print(" --------------------------------------------------------------")
                            sleep(2)
                            clear_screen()
                        else:
                            print(" ______________________________________________________________")
                            print("|                                                              |")
                            print(f"|     NO User found with user ID {user_to_delete}                           |")
                            print("|                                                              |")
                            print(" --------------------------------------------------------------")
                            sleep(2)
                            clear_screen()
                            break
                    elif choiceT == 3:
                        # Perform an aggregation query to calculate the total balance
                        pipeline = [
                            {
                                "$group": {
                                    "_id": None,
                                    "total_balance": {"$sum": "$balance"}
                                }
                            },
                            {
                                "$project": {
                                    "_id": 0
                                }
                            }
                        ]

                        total_balance_result = user_collection.aggregate(pipeline)
                        
                        # Extract the total balance from the result
                        total_balance = list(total_balance_result)[0]["total_balance"]
                        print("")
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|                   TOTAL USER BALANCE                         |")
                        print("|                                                              |")
                        print(f"|                 Total Balance = {total_balance}                       |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
                        input("Press enter to continue: ")
                        clear_screen()

                    elif choiceT == 4:
                        print(f"Enter the new Password for {admin['admin_id']}")
                        new_pass = input("Enter: ")
                        admin_collection.update_one({"admin_id": admin_id}, {"$set": {"password":new_pass}})
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|                 PASSWORD UPDATED SUCCESSFULLY                |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
                        subject = "Password Changed"
                        message = f"Your Admin account Password has been changed "
                        to_email = admin["gmail"]  # Replace with the user's email
                        send_email(subject, message, to_email)
                        sys.exit()
                    elif choiceT == 5:
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|                    EXITING ADMIN DASHBOARD                   |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
                        sys.exit()
                    else:
                        print(" ______________________________________________________________")
                        print("|                                                              |")
                        print("|                 PLEASE ENTER A VALID CHOICE                  |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
            else:
                print(" ______________________________________________________________")
                print("|                                                              |")
                print("|             Incorrect password. Login failed.                |")
                print("|                                                              |")
                print(" --------------------------------------------------------------")
                # Update login attempts and lock the account if needed
                admin_collection.update_one({"admin_id": admin_id}, {"$inc": {"login_attempts": 1}})
                login_attempts = admin_collection.find_one({"admin_id": admin_id})["login_attempts"]
                if login_attempts >= MAX_LOGIN_ATTEMPTS:
                    
                    print("  __________________________________________________________________________________________________")
                    print(" |                                                                                                  |")
                    print(f" |  Account locked for {LOCK_DURATION_SECONDS // 60} minutes due to too many failed login attempts. |")
                    print(" |                                                                                                  |")
                    print("  --------------------------------------------------------------------------------------------------")
                    admin_collection.update_one({"admin_id": admin_id}, {"$set": {"account_locked": True, "lock_time": int(time.time())}})
                    subject = "Account locked"
                    message = f"Your Admin account has been locked for 10 minutes. Due to too many failed login attempts.Try to login later"
                    to_email = admin["gmail"]  # Replace with the user's email
                    send_email(subject, message, to_email)
        else:
            lock_time = admin["lock_time"]
            current_time = int(time.time())
            if current_time - lock_time >= LOCK_DURATION_SECONDS:
                # Unlock the account if the lock duration has passed
                admin_collection.update_one({"admin_id": admin_id}, {"$set": {"account_locked": False,"lock_time":0,"login_attempts": 0}})
                print(" ______________________________________________________________")
                print("|                                                              |")
                print("|     Account unlocked. You may attempt to login later         |")
                print("|                                                              |")
                print(" --------------------------------------------------------------")
            else:
                remaining_lock_time = LOCK_DURATION_SECONDS - (current_time - lock_time)
                print("  ________________________________________________________________________")
                print(" |                                                                        |")
                print(f" | Account is locked. Try again after {remaining_lock_time // 60} minutes |")
                print(" |                                                                        |")
                print("  -------------------------------------------------------------------------")
    else:
        print(" ______________________________________________________________")
        print("|                                                              |")
        print("|        ADMIN not found. Please check your admin_id           |")
        print("|                                                              |")
        print(" --------------------------------------------------------------")

def userRegistration():
    user_count = countNumber(user_collection)
    if user_count >= 5:
        print(" ______________________________________________________________________")
        print("|                                                                      |")
        print("|             CANNOT ADD ANOTHER USER.LIMIT EXCEEDED                   |")
        print("|                                                                      |")
        print(" ---------------------------------------------------------------------")
        sys.exit()  # Use sys.exit() to exit the program
    while user_count < 6:
        unique_id = uuid.uuid4()
        unique_id_str = str(unique_id)
        user_id = unique_id_str[:4]
        print(" ______________________________________________________________")
        print("|                                                              |")
        print("|                 PLEASE ENTER USER DETAILS                    |")
        print("|                                                              |")
        print(" --------------------------------------------------------------")
        name = input("Enter the name of the user: ")
        password = input("Enter the password of the user: ")
        gmail = input("Please enter your gmail: ")
        clear_screen()
        unique = name.split()[0] + user_id
        data = {
            'name': name,
            'user_id': unique,
            'password': password,
            "login_attempts": 0, 
            "account_locked": False,
            "gmail":gmail,
            "balance":500
        }
        print("  ____________________________________________________________________________________________")
        print(" |                                                                                            |")
        print(F" |  User created Successfully and the user id is {unique} .Please use this id to login         |")
        print(" |                                                                                            |")
        print("  ---------------------------------------------------------------------------------------------")
        user_collection.insert_one(data)
        #Email messages 
        user = user_collection.find_one({"user_id": unique})
        subject = "Account Created"
        message = f"Your account has been successfully created.Your user id is: {unique}.Please use this id to login"
        to_email = user["gmail"]  # Replace with the user's email
        send_email(subject, message, to_email)
        clear_screen()
        print(" ______________________________________________________________________")
        print("|                                                                      |")
        print("|  If you want to add another user, press 'Y'. To exit, press 'N':     |")
        print("|                                                                      |")
        print("|                     PLEASE CHOOSE YOUR OPTION                        |")
        print(" ---------------------------------------------------------------------")
        another = input("Enter: ")
        clear_screen()
        if user_count >= 5:
            print(" ______________________________________________________________________")
            print("|                                                                      |")
            print("|             CANNOT ADD ANOTHER USER.LIMIT EXCEEDED                   |")
            print("|                                                                      |")
            print(" ---------------------------------------------------------------------")
            sys.exit()  # Use sys.exit() to exit the program
        if another.upper() != 'Y':
            break




def adminRegistration():
    admin_count = countNumber(admin_collection)
    if admin_count >= 1:
        print(" ______________________________________________________________________")
        print("|                                                                      |")
        print("|             CANNOT ADD ANOTHER ADMIN.LIMIT EXCEEDED                  |")
        print("|                                                                      |")
        print(" ---------------------------------------------------------------------")
        sys.exit()  # Use sys.exit() to exit the program
    while admin_count < 1:
        print(" ______________________________________________________________")
        print("|                                                              |")
        print("|                 PLEASE ENTER ADMIN DETAILS                   |")
        print("|                                                              |")
        print(" --------------------------------------------------------------")
        unique_id = uuid.uuid4()
        unique_id_str = str(unique_id)
        admin_id = unique_id_str[:4]
        name = input("Enter the name of the admin: ")
        password = input("Enter the password of the admin: ")
        gmail = input("Please enter your gmail: ")  
        clear_screen() 
        unique = name.split()[0] + admin_id 
        data = {
            'name': name,
            'admin_id': unique,
            'password': password,
            "login_attempts": 0, 
            "account_locked": False,
            "gmail":gmail
        }
        if data['name'] == "" or data['name'] == "" or data['name'] == "" :
            print(" ______________________________________________________________")
            print("|                                                              |")
            print("|             PLEASE ENTER CORRECT VALUES                      |")
            print("|                                                              |")
            print(" --------------------------------------------------------------")
            sys.exit()
        print("  ____________________________________________________________________________________________")
        print(" |                                                                                            |")
        print(f" | ADMIN ACC created Successfully and the user id is {unique} .Please use this id to login    |")
        print(" |                                                                                            |")
        print("  -------------------------------------------------------------------------------------------")
        admin_collection.insert_one(data)
        admin = admin_collection.find_one({"admin_id": unique})
        subject = "Account Created"
        message = f"Your account has been successfully created.Your admin id is: {unique}.Please use this id to login"
        to_email = admin["gmail"]  # Replace with the user's email
        send_email(subject, message, to_email)
        break

def main():
    print(" __________________________________________________")
    print("|                                                  |")
    print("|               WELCOME TO THE ATM                 |")
    print("|                                                  |")
    print("|               1. USER INTERFACE                  |")
    print("|                                                  |")
    print("|               2. ADMIN INTERFACE                 |")
    print("|                                                  |")
    print("|             PLEASE CHOOSE YOUR OPTION            |")
    print(" --------------------------------------------------")
    mainChoice = int(input("Enter: "))
    clear_screen()

    if mainChoice == 1:
        while True:
            print(" __________________________________________________")
            print("|                                                  |")
            print("|               1. REGISTER USER                   |")
            print("|                                                  |")
            print("|               2. USER LOGIN                      |")
            print("|                                                  |")
            print("|               3. EXIT                            |")
            print("|                                                  |")
            print("|             PLEASE CHOOSE YOUR OPTION            |")
            print(" --------------------------------------------------")
            choice = int(input("Enter: "))
            clear_screen()
            if choice == 1:
                userRegistration()
                break
            elif choice == 2:
                Userlogin()
            elif choice == 3:
                print(" ______________________________________________________________")
                print("|                                                              |")
                print("|                    EXITING USER DASHBOARD                    |")
                print("|                                                              |")
                print(" --------------------------------------------------------------")
                sys.exit()  # Use sys.exit() to exit the program
            else:
                print(" ______________________________________________________________")
                print("|                                                              |")
                print("|                 PLEASE ENTER A VALID CHOICE                  |")
                print("|                                                              |")
                print(" --------------------------------------------------------------")
    elif mainChoice == 2:
        print(" ______________________________________________________________")
        print("|                                                              |")
        print("|             WELCOME TO THE ADMIN DASHBOARD                   |")
        print("|                                                              |")
        print(" --------------------------------------------------------------")
        clear_screen()
        while True:
                print(" __________________________________________________")
                print("|                                                  |")
                print("|               1. REGISTER ADMIN                  |")
                print("|                                                  |")
                print("|               2. ADMIN LOGIN                     |")
                print("|                                                  |")
                print("|               3. EXIT                            |")
                print("|                                                  |")
                print("|             PLEASE CHOOSE YOUR OPTION            |")
                print(" --------------------------------------------------")
                choice = int(input("Enter: "))
                clear_screen()
                if choice == 1:
                    adminRegistration()
                    break
                elif choice == 2:
                    adminLogin()
                elif choice == 3:
                    print(" ______________________________________________________________")
                    print("|                                                              |")
                    print("|                    EXITING ADMIN DASHBOARD                   |")
                    print("|                                                              |")
                    print(" --------------------------------------------------------------")
                    sys.exit()  # Use sys.exit() to exit the program
                else:
                    print(" ______________________________________________________________")
                    print("|                                                              |")
                    print("|                 PLEASE ENTER A VALID CHOICE                  |")
                    print("|                                                              |")
                    print(" --------------------------------------------------------------")

if __name__ == "__main__":
    main()