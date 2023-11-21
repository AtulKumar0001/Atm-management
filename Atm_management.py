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

# library for timeout function 
import threading




# Connect to MongoDB Atlas. please replace this with your own
client = pymongo.MongoClient("Your connection String")
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



# Add a new field to the user and admin documents to track login attempts and lock status. (Not needed)
# user_collection.update_many({}, {"$set": {"login_attempts": 0, "account_locked": False}})
# admin_collection.update_many({}, {"$set": {"login_attempts": 0, "account_locked": False}})

# Define the number of allowed login attempts and lock duration
MAX_LOGIN_ATTEMPTS = 3
LOCK_DURATION_SECONDS = 600  # 10 minutes





# Time out function to stop execution if no input after 30 sec 

def user_input_thread(prompt):
    global user_input
    user_input = input(prompt)

def get_user_input_with_timeout(prompt, timeout):
    global user_input

    input_thread = threading.Thread(target=user_input_thread, args=(prompt,))
    input_thread.start()
    input_thread.join(timeout)

    if input_thread.is_alive():
        print("Timeout reached. Exiting program. You didn't enter any value.Please try again! ")
        input_thread.join()

    return user_input






#Function for Sending emails

def send_email(subject, message, to_email):
    from_email = "Your gmail"
    app_password = "Demo: bcdd azmj hssv dabt"  # generate from app password option in two step verification

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
        print(Fore.BLUE + " " + "_" * 55)
        print("|" + " " * 55 + "|")
        print(f"|                NO USER IS REGISTERED                  |")
        print("|" + " " * 55 + "|")
        print(Fore.BLUE + " " + "-" * 55 + Style.RESET_ALL)
        sys.exit()


    user_id = None
    password = None


    user_input1 = get_user_input_with_timeout("Please Enter your user_id: ", 30)
    if user_input1:
        user_id = user_input1

    user_input2 = get_user_input_with_timeout("Please Enter your password: ", 30)
    if user_input2:
        password = user_input2

    # old way 
    # user_id = input("Please enter your user_id: ")
    # password = input("Please enter your user password: ")


    clear_screen()
    
    # Search for the user by user_id
    user = user_collection.find_one({"user_id": user_id})

    if user:

        if not user["account_locked"] :
            stored_password = user["password"]

            if password == stored_password:
                print(Fore.BLUE + " " + "_" * 60)
                print("|" + " " * 60 + "|")
                print(f"|              Login successful. Welcome,  {user['name']}              |")
                print("|" + " " * 60 + "|")
                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                sleep(2)
                clear_screen()
                # Reset login attempts on successful login
                user_collection.update_one({"user_id": user_id}, {"$set": {"login_attempts": 0,"account_locked": False,"lock_time":0}})

                while True:
                    print(Fore.BLUE + " " + "_" * 50)
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "1. DEPOSIT MONEY" + " " * 19 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "2. WITHDRAW MONEY" + " " * 18 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "3. CHECK BALANCE" + " " * 19 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "4. CHANGE PASSWORD" + " " * 17 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "5. EXIT" + " " * 28 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 10 + "PLEASE CHOOSE YOUR OPTION" + " " * 15 + "|")
                    print(Fore.BLUE + " " + "-" * 50 + Style.RESET_ALL)
                    choiceT = int(input("Enter: "))
                    sleep(1)
                    clear_screen()
                    print("")

                    if choiceT == 1:
                        print(Fore.BLUE + " " + "_" * 70)
                        print("|" + " " * 70 + "|")
                        print("|                PLEASE ENTER THE AMOUNT YOU WANT TO DEPOSIT           |")
                        print("|" + " " * 70 + "|")
                        print("|" + " " * 25 + "DEPOSIT LIMIT IS 100K" + " " * 24 + "|")
                        print(Fore.BLUE + " " + "-" * 70 + Style.RESET_ALL)
                        amountD = int(input("Enter: "))
                        clear_screen()

                        if amountD <= 100000:
                            user_collection.update_one({"user_id": user_id}, {"$inc": {"balance":amountD}})
                            print("")
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 15 + Fore.BLUE + "AMOUNT DEPOSITED SUCCESSFULLY" + " " * 16 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            user = user_collection.find_one({"user_id": user_id})
                            subject = "Money Credited"
                            message = f"Your account is credited by INR {amountD}. ACC balance is {user['balance']} "
                            to_email = user["gmail"]  # Replace with the user's email
                            send_email(subject, message, to_email)
                            sys.exit()
                            break

                        else:
                            print(Fore.BLUE + " " + "_" * 55)
                        print("|" + " " * 55 + "|")
                        print("|" + " " * 15 + Fore.BLUE + "PLEASE ENTER WITHIN LIMIT" + " " * 15 + "|")
                        print("|" + " " * 55 + "|")
                        print(Fore.BLUE + " " + "-" * 55 + Style.RESET_ALL)

                    elif choiceT == 2:
                        print(Fore.BLUE + " " + "_" * 70)
                        print("|" + " " * 70 + "|")
                        print("|                PLEASE ENTER THE AMOUNT YOU WANT TO WITHDRAW          |")
                        print("|" + " " * 70 + "|")
                        print("|" + " " * 23 + "PLEASE CHOOSE YOUR OPTION" + " " * 22 + "|")
                        print(Fore.BLUE + " " + "-" * 70 + Style.RESET_ALL)
                        withdraw = int(input("Enter: "))

                        if withdraw <= 50000:
                            available = user["balance"]
                            if withdraw > available:
                                print(Fore.BLUE + " " + "_" * 50)
                                print("|" + " " * 50 + "|")
                                print("|" + " " * 16 + Fore.BLUE + "BALANCE IS LOW" + " " * 20 + "|")
                                print("|" + " " * 50 + "|")
                                print(Fore.BLUE + " " + "-" * 50 + Style.RESET_ALL)
                                sleep(4)
                                clear_screen()
                            else:
                                user_collection.update_one({"user_id": user_id}, {"$inc": {"balance":-withdraw}})
                                print(Fore.BLUE + " " + "_" * 60)
                                print("|" + " " * 60 + "|")
                                print("|" + " " * 16 + Fore.BLUE + "MONEY WITHDRAWN SUCCESSFULLY" + " " * 16 + "|")
                                print("|" + " " * 60 + "|")
                                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                                user = user_collection.find_one({"user_id": user_id})
                                subject = "Money Debited"
                                message = f"Your account is Debited by INR {withdraw}. ACC balance is {user['balance']} "
                                to_email = user["gmail"]  # Replace with the user's email
                                send_email(subject, message, to_email)
                                sys.exit()

                        else:
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 17 + Fore.BLUE + "PLEASE ENTER WITHIN LIMIT" + " " * 18 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                                                        # break

                    elif choiceT == 3:
                        # clear_screen()
                        print("")
                        user = user_collection.find_one({"user_id": user_id})
                        print(" ____________________________________________________________ṇ__")
                        print("|                                                              |")
                        print("|                   SHOWING USER BALANCE                       |")
                        print("|                                                              |")
                        print(f"|                 User_id = {user['user_id']}                           |")
                        print("|                                                              |")
                        print(f"|                 Balance = {user['balance']}                               |")
                        print("|                                                              |")
                        print(" --------------------------------------------------------------")
                        input("Press enter to continue: ")
                        # sleep(4)
                        clear_screen()

                    elif choiceT == 4:
                        oldPass = user["password"]
                        enteredOldPass = None
                        user_input_new = get_user_input_with_timeout(f"Please Enter your old password for {user['user_id']} : ", 30)

                        if user_input_new:
                            enteredOldPass = user_input_new
                        clear_screen()

                        if oldPass == enteredOldPass:

                            new_pass = None
                            user_input_new = get_user_input_with_timeout(f"Please Enter your new password for {user['user_id']} : ", 30)

                            if user_input_new:
                                new_pass = user_input_new

                            #old way
                            # print(f"Enter the new Password for {user['user_id']}")
                            # new_pass = input("Enter: ")

                            clear_screen()

                            

                            user_collection.update_one({"user_id": user_id}, {"$set": {"password":new_pass}})
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 16 + Fore.BLUE + "PASSWORD UPDATED SUCCESSFULLY" + " " * 15 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            subject = "Password Changed"
                            message = f"Your account Password has been changed "
                            to_email = user["gmail"]  # Replace with the user's email
                            send_email(subject, message, to_email)
                            sys.exit()

                        else:
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 15 + Fore.BLUE + "PASSWORD IS WRONG.TRY AGAIN" + " " * 18 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            sleep(4)
                            clear_screen()

                    elif choiceT == 5:
                        print(Fore.BLUE + " " + "_" * 60)
                        print("|" + " " * 60 + "|")
                        print("|" + " " * 20 + Fore.BLUE + "EXITING USER DASHBOARD" + " " * 18 + "|")
                        print("|" + " " * 60 + "|")
                        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                        sleep(4)
                        break

                    else:
                        print(Fore.BLUE + " " + "_" * 60)
                        print("|" + " " * 60 + "|")
                        print("|" + " " * 16 + Fore.BLUE + "PLEASE ENTER A VALID CHOICE" + " " * 17 + "|")
                        print("|" + " " * 60 + "|")
                        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                        sleep(2)
                
            else:
                
                print(Fore.BLUE + " " + "_" * 60)
                print("|" + " " * 60 + "|")
                print("|" + " " * 13 + Fore.BLUE + "Incorrect Password. Login failed" + " " * 15 + "|")
                print("|" + " " * 60 + "|")
                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                # Update login attempts and lock the account if needed
                user_collection.update_one({"user_id": user_id}, {"$inc": {"login_attempts": 1}})
                login_attempts = user_collection.find_one({"user_id": user_id})["login_attempts"]

                if login_attempts >= MAX_LOGIN_ATTEMPTS:
                    print(Fore.BLUE + " " + "_" * 84)
                    print("|" + " " * 84 + "|")
                    print(f"|       Account is locked for {remaining_lock_time // 60} minutes due to too many failed login attempts.       |")
                    print("|" + " " * 84 + "|")
                    print(Fore.BLUE + " " + "-" * 84 + Style.RESET_ALL)
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
                print(Fore.BLUE + " " + "_" * 62)
                print("|" + " " * 62 + "|")
                print("|" + " " * 7 + Fore.BLUE + "Account unlocked. You may attempt to login Now" + Fore.BLUE + " " * 9 + "|")
                print("|" + " " * 62 + "|")
                print(Fore.BLUE + " " + "-" * 62 + Style.RESET_ALL)

            else:
                remaining_lock_time = LOCK_DURATION_SECONDS - (current_time - lock_time)
                print(Fore.BLUE + " " + "_" * 75)
                print("|" + " " * 75 + "|")
                print(f"|                Account is locked. Try again after {remaining_lock_time // 60} minutes               |")
                print("|" + " " * 75 + "|")
                print(Fore.BLUE + " " + "-" * 75 + Style.RESET_ALL)

    else:
        print(Fore.BLUE + " " + "_" * 60)
        print("|" + " " * 60 + "|")
        print("|" + " " * 9 + Fore.BLUE + "USER not found. Please check your user_id" + " " * 10 + "|")
        print("|" + " " * 60 + "|")
        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)

# function for admin login 

def adminLogin():
    count = admin_collection.count_documents({})

    if count == 0:
        print(Fore.BLUE + " " + "_" * 55)
        print("|" + " " * 55 + "|")
        print(f"|                NO ADMIN IS REGISTERED                 |")
        print("|" + " " * 55 + "|")
        print(Fore.BLUE + " " + "-" * 55 + Style.RESET_ALL)
        sys.exit()

    admin_id = None
    password = None

    user_input1 = get_user_input_with_timeout("Please Enter your admin_id: ", 30)
    if user_input1:
        admin_id = user_input1

    user_input2 = get_user_input_with_timeout("Please Enter your password: ", 30)
    if user_input2:
        password = user_input2

    # old way 
    # admin_id = input("Please enter your admin_id: ")
    # password = input("Please enter your admin password: ")

    # Search for the admin by admin_id
    admin = admin_collection.find_one({"admin_id": admin_id})

    if admin:

        if  not admin["account_locked"]:
            stored_password = admin["password"]

            if password == stored_password:
                print(Fore.BLUE + " " + "_" * 60)
                print("|" + " " * 60 + "|")
                print(f"|              Login successful. Welcome,  {admin['name']}              |")
                print("|" + " " * 60 + "|")
                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                sleep(2)
                clear_screen()
                print("")
                # Reset login attempts on successful login
                admin_collection.update_one({"admin_id": admin_id}, {"$set": {"login_attempts": 0,"account_locked": False,"lock_time":0}})

                while True:
                    print(Fore.BLUE + " " + "_" * 50)
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "1. LOCK/UNLOCK USER ACC" + " " * 12 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "2. DELETE USER ACC" + " " * 17 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "3. CHECK BALANCE" + " " * 19 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "4. CHANGE PASSWORD" + " " * 17 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "5. CHANGE USER PASSWORD" + " " * 12 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "6. SHOW ALL USERS" + " " * 18 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "7. DEPOSIT MONEY" + " " * 19 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 15 + "8. EXIT" + " " * 28 + "|")
                    print("|" + " " * 50 + "|")
                    print("|" + " " * 10 + "PLEASE CHOOSE YOUR OPTION" + " " * 15 + "|")
                    print(Fore.BLUE + " " + "-" * 50 + Style.RESET_ALL)
                    choiceT = int(input("Enter: "))
                    clear_screen()

                    if choiceT == 1:
                        if user_collection.count_documents({}) == 0:
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 15 + Fore.BLUE + "There is no user registered. " + " " * 16 + "|")
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 10 + Fore.BLUE + "Please register any user and try again " + " " * 11 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            sleep(4)
                            clear_screen()
                            continue
                            # sys.exit()
                        oldPass = admin["password"]
                        enteredPass = None
                        user_input_new = get_user_input_with_timeout(f"Please Enter your password for {admin['admin_id']} : ", 30)

                        if user_input_new:
                            enteredPass = user_input_new
                        clear_screen()

                        if oldPass == enteredPass:
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 6 + Fore.BLUE + "PLEASE ENTER THE ACC ID YOU WANT TO LOCK\\UNLOCK" + " " * 7 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            acc = input("Enter: ")
                            clear_screen()
                            user = user_collection.find_one({"user_id": acc})
                            print(Fore.BLUE + " " + "_" * 70)
                            print("|" + " " * 70 + "|")
                            print("|     If you want to Lock user, press 'L'. To Unlock, press 'U':       |")
                            print("|" + " " * 70 + "|")
                            print("|" + " " * 21 + "PLEASE CHOOSE YOUR OPTION" + " " * 24 + "|")
                            print(Fore.BLUE + " " + "-" * 70 + Style.RESET_ALL)
                            option = input("Enter: ")
                            clear_screen()

                            if user and option.upper() == 'L':
                                user_collection.update_one({"user_id": acc}, {"$set": {"account_locked":True,"lock_time": int(time.time())}})
                                print("")
                                print(Fore.BLUE + " " + "_" * 60)
                                print("|" + " " * 60 + "|")
                                print("|" + " " * 15 + Fore.BLUE + "ACCOUNT LOCKED SUCCESSFULLY  " + " " * 16 + "|")
                                print("|" + " " * 60 + "|")
                                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)

                                # admin = admin_collection.find_one({"admin_id": admin_id})
                                # subject = "Money Credited"
                                # message = f"Your Admin account is credited by INR {amountD}. ACC balance is {admin['balance']} "
                                # to_email = admin["gmail"]  # Replace with the user's email
                                # send_email(subject, message, to_email)
                                # sys.exit()
                                # break

                            elif user and option.upper() == 'U':
                                user_collection.update_one({"user_id": acc}, {"$set": {"account_locked":False,"lock_time":0}})
                                print("")
                                print(Fore.BLUE + " " + "_" * 60)
                                print("|" + " " * 60 + "|")
                                print("|" + " " * 15 + Fore.BLUE + "ACCOUNT UNLOCKED SUCCESSFULLY  " + " " * 14 + "|")
                                print("|" + " " * 60 + "|")
                                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)

                            else:
                                print(Fore.BLUE + " " + "_" * 60)
                                print("|" + " " * 60 + "|")
                                print("|" + " " * 15 + Fore.BLUE + "PLEASE ENTER CORRECT USER ID " + " " * 16 + "|")
                                print("|" + " " * 60 + "|")
                                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)

                        else:
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 15 + Fore.BLUE + "PASSWORD IS WRONG.TRY AGAIN" + " " * 18 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            sleep(4)
                            clear_screen()


                    elif choiceT == 2:
                        if user_collection.count_documents({}) == 0:
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 15 + Fore.BLUE + "There is no user registered. " + " " * 16 + "|")
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 10 + Fore.BLUE + "Please register any user and try again " + " " * 11 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            # sys.exit()
                            sleep(4)
                            clear_screen()
                            continue
                        oldPass = admin["password"]
                        enteredPass = None
                        user_input_new = get_user_input_with_timeout(f"Please Enter your password for {admin['admin_id']} : ", 30)

                        if user_input_new:
                            enteredPass = user_input_new
                        clear_screen()

                        if oldPass == enteredPass:

                            print("Are you sure you want to Delete?. You cannot Redo this Action!")
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 9 + Fore.BLUE + "PLEASE ENTER THE ACC ID YOU WANT TO DELETE" + " " * 9 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)

                            user_to_delete = input("Enter the user ID you want to delete: ")

                            # Perform the delete operation
                            result = user_collection.delete_one({"user_id": user_to_delete})

                            # Check if the delete operation was successful
                            if result.deleted_count == 1:
                                print(Fore.BLUE + " " + "_" * 60)
                                print("|" + " " * 60 + "|")
                                print(f"|     User with user ID {user_to_delete} has been deleted             |")
                                print("|" + " " * 60 + "|")
                                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                                sleep(4)
                                clear_screen()

                            else:
                                print(Fore.BLUE + " " + "_" * 60)
                                print("|" + " " * 60 + "|")
                                print(f"|         NO User found with user ID {user_to_delete}            |")
                                print("|" + " " * 60 + "|")
                                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                                sleep(5)
                                clear_screen()
                                # break
                        else:
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 15 + Fore.BLUE + "PASSWORD IS WRONG.TRY AGAIN" + " " * 18 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            sleep(4)
                            clear_screen()

                    elif choiceT == 3:
                        if user_collection.count_documents({}) == 0:
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 15 + Fore.BLUE + "There is no user registered. " + " " * 16 + "|")
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 10 + Fore.BLUE + "Please register any user and try again " + " " * 11 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            # sys.exit()
                            sleep(4)
                            clear_screen()
                            continue
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
                        pipeline2 = [
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
                        total_balance_result2 = admin_collection.aggregate(pipeline)
                        
                        # Extract the total balance from the result
                        total_balance = list(total_balance_result)[0]["total_balance"] + list(total_balance_result2)[0]["total_balance"]
                        if total_balance < 75000:
                            print("")
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 14 + Fore.BLUE + "Total Account balance is below 75k " + " " * 11 + "|")
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 17 + Fore.BLUE + "Please Deposit some amount " + " " * 16 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                        else:
                            print("")
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 59 + "|")
                            print("|" + " " * 22 + Fore.BLUE + "TOTAL BALANCE" + " " * 24 + "|")
                            print("|" + " " * 59 + "|")
                            print(f"|                  Total Balance = {total_balance}                    |")
                            print("|" + " " * 59 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            input("Press enter to continue: ")
                            clear_screen()

                    elif choiceT == 4:
                        new_pass = None
                        user_input_new = get_user_input_with_timeout(f"Please Enter your new password for {admin['admin_id']} : ", 30)
                        if user_input_new:
                            new_pass = user_input_new
                        clear_screen()

                        # old way 
                        # print(f"Enter the new Password for {admin['admin_id']}")
                        # new_pass = input("Enter: ")

                        admin_collection.update_one({"admin_id": admin_id}, {"$set": {"password":new_pass}})
                        print(Fore.BLUE + " " + "_" * 60)
                        print("|" + " " * 60 + "|")
                        print("|" + " " * 16 + Fore.BLUE + "PASSWORD UPDATED SUCCESSFULLY" + " " * 15 + "|")
                        print("|" + " " * 60 + "|")
                        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                        subject = "Password Changed"
                        message = f"Your Admin account Password has been changed "
                        to_email = admin["gmail"]  # Replace with the user's email
                        send_email(subject, message, to_email)
                        sys.exit()

                    elif choiceT == 5:

                        if user_collection.count_documents({}) == 0:
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 15 + Fore.BLUE + "There is no user registered " + " " * 17 + "|")
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 10 + Fore.BLUE + "Please register any user and try again." + " " * 11 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            sleep(4)
                            clear_screen()
                            continue

                        oldPass = admin["password"]
                        enteredPass = None
                        user_input_new = get_user_input_with_timeout(f"Please Enter your password for {admin['admin_id']} : ", 30)

                        if user_input_new:
                            enteredPass = user_input_new
                        clear_screen()

                        if oldPass == enteredPass:
                        
                            user_id = None

                            user_input1 = get_user_input_with_timeout("Please Enter your user_id: ", 30)
                            if user_input1:
                                user_id = user_input1

                            clear_screen()
        
                            # Search for the user by user_id
                            user = user_collection.find_one({"user_id": user_id})
                            if not user:
                                print(Fore.BLUE + " " + "_" * 60)
                                print("|" + " " * 60 + "|")
                                print("|" + " " * 16 + Fore.BLUE + "PLEASE ENTER CORRECT USER ID" + " " * 16 + "|")
                                print("|" + " " * 60 + "|")
                                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                                sleep(3)
                                clear_screen()
                            else:
                                new_pass = None
                                user_input_new = get_user_input_with_timeout(f"Please Enter your new password for {user['user_id']} : ", 30)

                                if user_input_new:
                                    new_pass = user_input_new

                                #old way
                                # print(f"Enter the new Password for {user['user_id']}")
                                # new_pass = input("Enter: ")

                                clear_screen()
                                user_collection.update_one({"user_id": user_id}, {"$set": {"password":new_pass}})
                                print(Fore.BLUE + " " + "_" * 60)
                                print("|" + " " * 60 + "|")
                                print("|" + " " * 16 + Fore.BLUE + "PASSWORD UPDATED SUCCESSFULLY" + " " * 15 + "|")
                                print("|" + " " * 60 + "|")
                                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                                subject = "Password Changed"
                                message = f"Your User account Password has been changed by the admin. For any query please contact to your admin"
                                to_email = user["gmail"]  # Replace with the user's email
                                send_email(subject, message, to_email)
                                # sys.exit()
                                sleep(4)
                                clear_screen()
                        else:
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 16 + Fore.BLUE + "PASSWORD IS WRONG.TRY AGAIN." + " " * 16 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            sleep(4)
                            clear_screen()
                    elif choiceT == 6:
                        if user_collection.count_documents({}) == 0:
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 15 + Fore.BLUE + "There is no user registered " + " " * 17 + "|")
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 10 + Fore.BLUE + "Please register any user and try again." + " " * 11 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            sleep(4)
                            clear_screen()
                            continue
                        # Fetch all user records from the collection
                        users = user_collection.find({})

                        # Iterate through each user and print the desired fields
                        for user in users:
                            print("----------------------------")
                            print("Name:", user["name"])
                            print("User ID:", user["user_id"])
                            print("Gmail:", user["gmail"])
                            print("Balance:", user["balance"])
                            print("----------------------------")
                            print()  # Empty line for readability
                    elif choiceT == 7:
                        print(Fore.BLUE + " " + "_" * 60)
                        print("|" + " " * 60 + "|")
                        print("|" + " " * 7 + Fore.BLUE + "PLEASE ENTER THE AMOUNT YOU WANT TO DEPOSIT " + " " * 9 + "|")
                        print("|" + " " * 60 + "|")
                        print("|" + " " * 19 + Fore.BLUE + "DEPOSIT LIMIT IS 300K " + " " * 19 + "|")
                        print("|" + " " * 60 + "|")
                        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                        amount = int(input("Enter: "))
                        clear_screen()

                        # # Perform an aggregation query to calculate the total balance
                        # pipeline = [
                        #     {
                        #         "$group": {
                        #             "_id": None,
                        #             "total_balance": {"$sum": "$balance"}
                        #         }
                        #     },
                        #     {
                        #         "$project": {
                        #             "_id": 0
                        #         }
                        #     }
                        # ]

                        # total_balance_result = user_collection.aggregate(pipeline)
                        
                        # Extract the total balance from the result
                        balance = admin_collection.find_one({},{"_id":0,"balance":1})
                        total_balance = balance['balance']
                        if amount <= 300000 and total_balance < 300000:
                            admin_collection.update_one({"admin_id": admin_id}, {"$inc": {"balance":amount}})
                            print("")
                            print(Fore.BLUE + " " + "_" * 60)
                            print("|" + " " * 60 + "|")
                            print("|" + " " * 15 + Fore.BLUE + "AMOUNT DEPOSITED SUCCESSFULLY" + " " * 16 + "|")
                            print("|" + " " * 60 + "|")
                            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                            admin = admin_collection.find_one({"admin_id": admin_id})
                            subject = "Money Credited"
                            message = f"Your account is credited by INR {amount}. ACC balance is {admin['balance']} "
                            to_email = admin["gmail"]  # Replace with the user's email
                            send_email(subject, message, to_email)
                            sys.exit()
                            break
                        else:
                            print(Fore.BLUE + " " + "_" * 75)
                            print("|" + " " * 75 + "|")
                            print("|" + " " * 10 + Fore.BLUE + "PLEASE ENTER WITHIN LIMIT OR CHECK ACCOUNT TOTAL LIMIT " + " " * 10 + "|")
                            print("|" + " " * 75 + "|")
                            print(Fore.BLUE + " " + "-" * 75 + Style.RESET_ALL)

                    elif choiceT == 8:
                        print(Fore.BLUE + " " + "_" * 60)
                        print("|" + " " * 60 + "|")
                        print("|" + " " * 18 + Fore.BLUE + "EXITING ADMIN DASHBOARD" + " " * 19 + "|")
                        print("|" + " " * 60 + "|")
                        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                        sleep(2)
                        break

                    else:
                        print(Fore.BLUE + " " + "_" * 60)
                        print("|" + " " * 60 + "|")
                        print("|" + " " * 15 + Fore.BLUE + "PLEASE ENTER A VALID CHOICE" + " " * 18 + "|")
                        print("|" + " " * 60 + "|")
                        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)


            else:
                print(Fore.BLUE + " " + "_" * 60)
                print("|" + " " * 60 + "|")
                print("|" + " " * 13 + Fore.BLUE + "Incorrect Password. Login failed" + " " * 15 + "|")
                print("|" + " " * 60 + "|")
                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                # Update login attempts and lock the account if needed
                admin_collection.update_one({"admin_id": admin_id}, {"$inc": {"login_attempts": 1}})
                login_attempts = admin_collection.find_one({"admin_id": admin_id})["login_attempts"]

                if login_attempts >= MAX_LOGIN_ATTEMPTS:
                    
                    print(Fore.BLUE + " " + "_" * 84)
                    print("|" + " " * 84 + "|")
                    print(f"|       Account is locked for {remaining_lock_time // 60} minutes due to too many failed login attempts.       |")
                    print("|" + " " * 84 + "|")
                    print(Fore.BLUE + " " + "-" * 84 + Style.RESET_ALL)
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
                print(Fore.BLUE + " " + "_" * 60)
                print("|" + " " * 60 + "|")
                print(f"|       Account unlocked. You may now attempt to login       |")
                print("|" + " " * 60 + "|")
                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)

            else:
                remaining_lock_time = LOCK_DURATION_SECONDS - (current_time - lock_time)
                print(Fore.BLUE + " " + "_" * 60)
                print("|" + " " * 60 + "|")
                print(f"|       Account is locked. Try again after {remaining_lock_time // 60} minutes         |")
                print("|" + " " * 60 + "|")
                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)

    else:
        print(Fore.BLUE + " " + "_" * 60)
        print("|" + " " * 60 + "|")
        print("|" + " " * 8 + Fore.BLUE + "ADMIN not found. Please check your admin_id" + " " * 9 + "|")
        print("|" + " " * 60 + "|")
        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)

def userRegistration():
    user_count = countNumber(user_collection)
    if user_count >= 5:
        print(Fore.BLUE + " " + "_" * 60)
        print("|" + " " * 60 + "|")
        print("|" + " " * 10 + Fore.BLUE + "CANNOT ADD ANOTHER USER. LIMIT EXCEEDED" + " " * 11 + "|")
        print("|" + " " * 60 + "|")
        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
        sys.exit()  # Use sys.exit() to exit the program

    while user_count < 6:
        if admin_collection.count_documents({}) == 0:
            print(Fore.BLUE + " " + "_" * 60)
            print("|" + " " * 60 + "|")
            print("|" + " " * 18 + Fore.BLUE + "PLEASE ENTER ADMIN FIRST" + " " * 18 + "|")
            print("|" + " " * 60 + "|")
            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
            sys.exit()
        unique_id = uuid.uuid4()
        unique_id_str = str(unique_id)
        user_id = unique_id_str[:4]
        print(Fore.BLUE + " " + "_" * 60)
        print("|" + " " * 60 + "|")
        print("|" + " " * 17 + Fore.BLUE + "PLEASE ENTER USER DETAILS" + " " * 18 + "|")
        print("|" + " " * 60 + "|")
        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
        name = input("Enter the name of the user: ")
        password = input("Enter the password of the user: ")
        gmail = input("Please enter your gmail: ")
        clear_screen()

        if name == "" or password == "" or gmail == "" :
            print(Fore.BLUE + " " + "_" * 60)
            print("|" + " " * 60 + "|")
            print("|" + " " * 15 + Fore.BLUE + "PLEASE ENTER CORRECT VALUES" + " " * 18 + "|")
            print("|" + " " * 60 + "|")
            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
            sys.exit()
        unique = name.split()[0] + user_id
        data = {
            'name': name,
            'user_id': unique,
            'password': password,
            "login_attempts": 0, 
            "account_locked": False,
            "gmail":gmail,
            "balance":5000
        }
        print(Fore.BLUE + " " + "_" * 89)
        print("|" + " " * 89 + "|")
        print(f"|USER ACC created Successfully and the user id is {unique}. Please use this id to login   |")
        print("|" + " " * 89 + "|")
        print(Fore.BLUE + " " + "-" * 89 + Style.RESET_ALL)
        user_collection.insert_one(data)
        #Email messages 
        user = user_collection.find_one({"user_id": unique})
        subject = "Account Created"
        message = f"Your account has been successfully created.Your user id is: {unique}.Please use this id to login"
        to_email = user["gmail"]  # Replace with the user's email
        send_email(subject, message, to_email)
        clear_screen()
        print(Fore.BLUE + " " + "_" * 70)
        print("|" + " " * 70 + "|")
        print("|  If you want to add another user, press 'Y'. To exit, press 'N':     |")
        print("|" + " " * 70 + "|")
        print("|" + " " * 21 + "PLEASE CHOOSE YOUR OPTION" + " " * 24 + "|")
        print(Fore.BLUE + " " + "-" * 70 + Style.RESET_ALL)
        another = input("Enter: ")
        clear_screen()

        if user_count >= 5:
            print(Fore.BLUE + " " + "_" * 60)
            print("|" + " " * 60 + "|")
            print("|" + " " * 10 + Fore.BLUE + "CANNOT ADD ANOTHER USER. LIMIT EXCEEDED" + " " * 11 + "|")
            print("|" + " " * 60 + "|")
            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
            sys.exit()  # Use sys.exit() to exit the program

        if another.upper() != 'Y':
            break




def adminRegistration():
    admin_count = countNumber(admin_collection)
    if admin_count >= 1:
        print(Fore.BLUE + " " + "_" * 60)
        print("|" + " " * 60 + "|")
        print("|" + " " * 10 + Fore.BLUE + "CANNOT ADD ANOTHER ADMIN. LIMIT EXCEEDED" + " " * 10 + "|")
        print("|" + " " * 60 + "|")
        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
        sys.exit()  # Use sys.exit() to exit the program

    while admin_count < 1:
        print(Fore.BLUE + " " + "_" * 60)
        print("|" + " " * 60 + "|")
        print("|" + " " * 15 + Fore.BLUE + "PLEASE ENTER ADMIN DETAILS" + " " * 19 + "|")
        print("|" + " " * 60 + "|")
        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
        unique_id = uuid.uuid4()
        unique_id_str = str(unique_id)
        admin_id = unique_id_str[:4]
        name = input("Enter the name of the admin: ")
        password = input("Enter the password of the admin: ")
        gmail = input("Please enter your gmail: ")  
        clear_screen() 

        if name == "" or password == "" or gmail == "" :
            print(Fore.BLUE + " " + "_" * 60)
            print("|" + " " * 60 + "|")
            print("|" + " " * 15 + Fore.BLUE + "PLEASE ENTER CORRECT VALUES" + " " * 18 + "|")
            print("|" + " " * 60 + "|")
            print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
            sys.exit()
        unique = name.split()[0] + admin_id 
        data = {
            'name': name,
            'admin_id': unique,
            'password': password,
            "login_attempts": 0, 
            "account_locked": False,
            "balance":50000,
            "gmail":gmail
        }
        
        print(Fore.BLUE + " " + "_" * 89)
        print("|" + " " * 89 + "|")
        print(f"|ADMIN ACC created Successfully and the ADMIN id is {unique}. Please use this id to login |")
        print("|" + " " * 89 + "|")
        print(Fore.BLUE + " " + "-" * 89 + Style.RESET_ALL)
        admin_collection.insert_one(data)
        admin = admin_collection.find_one({"admin_id": unique})
        subject = "Account Created"
        message = f"Your account has been successfully created.Your admin id is: {unique}.Please use this id to login"
        to_email = admin["gmail"]  # Replace with the user's email
        send_email(subject, message, to_email)
        break

def main():
    print(Fore.BLUE + " " + "_" * 50)
    print("|" + " " * 50 + "|")
    print("|" + " " * 15 + Fore.BLUE + "WELCOME TO THE ATM" + " " * 17 + "|")
    print("|" + " " * 50 + "|")
    print("|" + " " * 12 + "1. USER INTERFACE" + " " * 21 + "|")
    print("|" + " " * 50 + "|")
    print("|" + " " * 12 + "2. ADMIN INTERFACE" + " " * 20 + "|")
    print("|" + " " * 50 + "|")
    print("|" + " " * 12 + "3. EXIT" + " " * 31 + "|")
    print("|" + " " * 50 + "|")
    print("|" + " " * 12 + "PLEASE CHOOSE YOUR OPTION" + " " * 13 + "|")
    print(Fore.BLUE + " " + "-" * 50 + Style.RESET_ALL)
    mainChoice = int(input("Enter: "))
    clear_screen()

    if mainChoice == 1:

        while True:
            print(Fore.BLUE + " " + "_" * 50)
            print("|" + " " *50 + "|")
            print("|" + " " * 15 + Fore.BLUE + "1. REGISTER USER" + " " * 19 + "|")
            print("|" + " " * 50 + "|")
            print("|" + " " * 15 + Fore.BLUE + "2. USER LOGIN" + " " * 22 + "|")
            print("|" + " " * 50 + "|")
            print("|" + " " * 15 + Fore.BLUE + "3. EXIT" + " " * 28 + "|")
            print("|" + " " * 50 + "|")
            print("|" + " " * 15 + Fore.BLUE + "PLEASE CHOOSE YOUR OPTION" + " " * 10 + "|")
            print(Fore.BLUE + " " + "-" * 50 + Style.RESET_ALL)
            choice = int(input("Enter: "))
            clear_screen()

            if choice == 1:
                userRegistration()

            elif choice == 2:
                Userlogin()
                

            elif choice == 3:
                print(Fore.BLUE + " " + "_" * 60)
                print("|" + " " * 60 + "|")
                print("|" + " " * 20 + Fore.BLUE + "EXITING USER DASHBOARD" + " " * 18 + "|")
                print("|" + " " * 60 + "|")
                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                main()  

            else:
                print(Fore.BLUE + " " + "_" * 60)
                print("|" + " " * 60 + "|")
                print("|" + " " * 16 + Fore.BLUE + "PLEASE ENTER A VALID CHOICE" + " " * 17 + "|")
                print("|" + " " * 60 + "|")
                print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)

    elif mainChoice == 2:
        print(Fore.BLUE + " " + "_" * 60)
        print("|" + " " * 60 + "|")
        print("|" + " " * 15 + Fore.BLUE + "WELCOME TO THE ADMIN DASHBOARD" + " " * 15 + "|")
        print("|" + " " * 60 + "|")
        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
        clear_screen()

        while True:
                print(Fore.BLUE + " " + "_" * 50)
                print("|" + " " *50 + "|")
                print("|" + " " * 15 + Fore.BLUE + "1. REGISTER ADMIN" + " " * 18 + "|")
                print("|" + " " * 50 + "|")
                print("|" + " " * 15 + Fore.BLUE + "2. ADMIN LOGIN" + " " * 21 + "|")
                print("|" + " " * 50 + "|")
                print("|" + " " * 15 + Fore.BLUE + "3. EXIT" + " " * 28 + "|")
                print("|" + " " * 50 + "|")
                print("|" + " " * 15 + Fore.BLUE + "PLEASE CHOOSE YOUR OPTION" + " " * 10 + "|")
                print(Fore.BLUE + " " + "-" * 50 + Style.RESET_ALL)
                choice = int(input("Enter: "))
                clear_screen()
                if choice == 1:
                    adminRegistration()
                elif choice == 2:
                    adminLogin()
                    
                elif choice == 3:
                    print(Fore.BLUE + " " + "_" * 60)
                    print("|" + " " * 60 + "|")
                    print("|" + " " * 15 + Fore.BLUE + "EXITING ADMIN DASHBOARD" + " " * 22 + "|")
                    print("|" + " " * 60 + "|")
                    print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
                    main() 
                else:
                    print(Fore.BLUE + " " + "_" * 60)
                    print("|" + " " * 60 + "|")
                    print("|" + " " * 15 + Fore.BLUE + "PLEASE ENTER A VALID CHOICE" + " " * 18 + "|")
                    print("|" + " " * 60 + "|")
                    print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
    elif mainChoice == 3:
        print(Fore.BLUE + " " + "_" * 60)
        print("|" + " " * 60 + "|")
        print("|" + " " * 18 + Fore.BLUE + "EXITING DASHBOARD" + " " * 25 + "|")
        print("|" + " " * 60 + "|")
        print(Fore.BLUE + " " + "-" * 60 + Style.RESET_ALL)
        sleep(2)
        sys.exit()

        
if __name__ == "__main__":
    main()
    init()
