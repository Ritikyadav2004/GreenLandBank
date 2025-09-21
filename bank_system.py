import termcolor
import time
import os   #  os.system('cls' if os.name == 'nt' else 'clear') code for clear screen
from colorama import init, Fore, Back, Style
import bcrypt
import random
import mysql.connector
autocommit=False  # <-- Add this line to disable autocommit
conn = mysql.connector.connect(
    host='localhost',
    password='Ritik@2004',
    user='root',
    database='bank' #bank me bankdatas
    )
cur=conn.cursor()
#Function to login into account
def login():
    acno = input("Enter your account number: ")
    
    # Execute a query to search for the account number
    query = "SELECT * FROM bankdatas WHERE acno = %s"
    cur.execute(query, [acno])
    
    # Fetch the result
    result = cur.fetchall()
    
    # If account number is found
    if result:
       # pin1 = int(input("Enter your PIN: "))
       pin_to_check = input("Enter your PIN: ").encode('utf-8')
       hashed_pin_from_db = result[0][9]
        
        # Check if the PIN is correct
       if bcrypt.checkpw(pin_to_check, hashed_pin_from_db):
        #if pin1 == result[0][9]:  # type: ignore # assuming PIN is stored in the 6th column
            # Print all details of the person
            print_cyan("Account Login Succesfully\n")  
            print_green("Account Details:")
            print("Account Number:", result[0][2])
            print("Name          :", result[0][1])
            print("Address       :", result[0][5])
            print("Balance       :", result[0][3])
             
               
            
       else:
            print("Invalid PIN")
            #sfun()
            
    else:
        print("Account number not found")
        



def transferMoney():
    acno = input("Enter Your Account Number :")  # Account Number of Sender
    query = "SELECT * FROM BANKDATAS WHERE acno=%s"
    cur.execute(query, [acno])
    result = cur.fetchall() # Use fetchone() as we expect only one row
    
    if result:
        # Use a consistent and explicit column name for PIN
        pin_to_check = input("Enter your PIN: ").encode('utf-8')
        hashed_pin_from_db = result[0][9]
        
        if bcrypt.checkpw(pin_to_check, hashed_pin_from_db):
            print_cyan("Account Login Successful\n")
            
            acno_transfer = input("Enter A/C no to transfer Rupee :")
            query1 = "SELECT * FROM BANKDATAS WHERE acno=%s"
            cur.execute(query1, [acno_transfer])
            result1 = cur.fetchall()
            
            if result1:
                transfer_amount = float(input("Enter amount : "))
                
                if transfer_amount <= 0:
                    print_red("Invalid Amount\n\n")
                    time.sleep(3)
                    run_program()
                else:
                    try:
                        conn.autocommit = True
                        conn.start_transaction()
                        
                        # Use a more explicit UPDATE query for safety
                        # This single query checks for funds and debits the account atomically
                        query_debit = "UPDATE bankdatas SET Deposit = Deposit - %s WHERE acno = %s AND Deposit >= %s"
                        cur.execute(query_debit, (transfer_amount, acno, transfer_amount))
                        
                        # The `rowcount` property tells us how many rows were affected
                        if cur.rowcount == 0:
                            raise ValueError("Insufficient funds or account not found for debit.")

                        query_credit = "UPDATE bankdatas SET Deposit = Deposit + %s WHERE acno = %s"
                        cur.execute(query_credit, (transfer_amount, acno_transfer))
                        
                        conn.commit()
                        
                        # Fetch the new balance AFTER a successful commit
                        cur.execute("SELECT Deposit FROM BANKDATAS WHERE acno = %s", [acno])
                        new_balance = cur.fetchall()[0]
                        
                        print_green("Transaction Successful!")
                        print(f"Available balance: {new_balance}")

                    except (mysql.connector.Error, ValueError) as err:
                        conn.rollback()
                        print_red(f"Transaction Failed: {err}")
            else:
                print_red("Receiver Account Number Not Found")
        else:
            print_red("\nIncorrect Pin. Try again!\n")
    else:
        print_red("\nIncorrect Account Number\n")

        
    
def getinfo(): #option 1 to creating account
    a2=random.randint(10000000,99999999)
    c1=int(input("Mobile number:"))
    print("OTP has been sent successfuly")
    d=int(input("--->"))
    a=input("Enter Your Name :")
    b=input("DOB in Format--> dd-mm-yy    :")
    c=input("Permanent Address :")
    e=int(input("Adhar No :"))
    d=input("E-mail  :")
    f=float(input("Add Money :")) #changed int-->float
   # g=int(input("create 4 digit security pin\n--->"))
    pin = input("Create 4 digit security pin: ").encode('utf-8') 
    hashed_pin = bcrypt.hashpw(pin, bcrypt.gensalt())
    print_green("\n                   Congratulations! Mr/Mrs " + a + " your account created sucessfully\n")
    print_green("Your account number is : " + str(a2))
    print_magenta("\nPress 1 to Genrate E-Passbook :")
    h=int(input("--->"))
    t=(a,a2,f,b,c,d,e,c1,hashed_pin) 
    s="Insert into bankdatas(Name, Acno,Deposit,dob,Address,email,Adhar_no,Mobile,Pin) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(s,t)
    conn.commit()
    if(h==1):
        print("Name           :",a)
        print("Account Number :",a2)
        print("Deposit        :",f)
        print("DOB            :",b)
        print("Address        :",c)
        print("E-mal id       :",d)
    else:
        # run_program()
        print_red("invalid choice")

def print_red(text):
    print(termcolor.colored(text, 'red'))

def print_green(text):
    print(termcolor.colored(text, 'green'))

def print_yellow(text):
    print(termcolor.colored(text, 'yellow'))

def print_blue(text):
    print(termcolor.colored(text, 'blue'))

def print_magenta(text):
    print(termcolor.colored(text, 'magenta'))

def print_cyan(text):
    print(termcolor.colored(text, 'cyan'))

import os
from colorama import init, Fore, Back, Style

init()  # Initialize colorama

def display_advertisement():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
    print(Back.BLACK + """
_____________________________________________________
              """ + Fore.GREEN + """          GREENLAND BANK          """ + Fore.WHITE + """
_____________________________________________________

-->Open a new account today and get a chance to win a FREE IPAD!
-->Deposit ₹75,000 and get a ₹3,750 bonus!
-->Refer a friend and get a ₹1,500 credit!
-->Visit our website or branch today to learn more!

_____________________________________________________
              """ + Fore.GREEN + """  Your Partner in Success  """ + Fore.WHITE + """
_____________________________________________________
""" + Style.RESET_ALL)
   
def invalid_selection():
    print_red('Please try again,  Check your input.')

def main_menu():
    #display_advertisement()
    print_yellow('Please choose an option:')
    print(' ')
    print_cyan('1. Open a new account')
    print_cyan('2. Login')
    print_cyan('3. Withdraw funds')
    print_cyan('4. Check account balance')
    print_cyan('5. Deposit')
    print_cyan('6. Transfer Money Through A/C No.') #addition of transfer
    print_red('7. Exit')
    print(' ')

def run_program():
   
    display_advertisement()
    
    while True:#it is the main loop which run program untill user want 
        main_menu()
        try:
            user_selection = int(input('Enter your selection (1-7):\n--->'))
            if user_selection == 1:
                print_green('You selected: Open a new account')
                getinfo()
                # Add code here to open a new account
            elif user_selection == 2:
                print_cyan('You selected: Login ')
                login()
                
          
            elif user_selection == 3:  #withdraw money
                print_magenta('You selected: Withdraw funds')
                # Add code here to process a withdrawa
                z2=input("Enter Your Account No\n--->")
                
                query = "SELECT * FROM bankdatas WHERE acno = %s"
                cur.execute(query, [z2])
                result = cur.fetchall()
                if result:
                    pin_to_check = input("Enter your PIN: ").encode('utf-8')
                    hashed_pin_from_db = result[0][9]
                    if bcrypt.checkpw(pin_to_check, hashed_pin_from_db):
                    #if pin2 == result[0][9]:
                        amount = float(input("Enter the amount to withdraw: "))
                        if(amount<=0):
                            print_red("Invalid Amount\n\n")
                            time.sleep(3)
                            run_program()
                        elif result[0][3] < amount:
                            print_red("Not enough money in your account.")
                            time.sleep(3)
                            run_program()

                            
                    else:
                        print_red("Incorrect PIN\n\n")
                        time.sleep(3)
                        run_program()
                               
                   

    # Update the account balance
                    query = "UPDATE bankdatas SET deposit = deposit - %s WHERE acno = %s"
                    cur.execute(query, (amount, z2))#z2 is account number
                    print_green("Amount Successfully Withdraw \nBalance--->")
                    conn.commit()
                    print(result[0][3]-amount)
            elif user_selection == 4:                       #DOne
                print_yellow('You selected: Check account balance')
                z1=input("Enter Your Account No\n--->")
                query = "SELECT * FROM bankdatas WHERE acno = %s"
                cur.execute(query, [z1])
                result = cur.fetchall()
                if result:
                    pin_to_check = input("Enter your PIN: ").encode('utf-8')
                    hashed_pin_from_db = result[0][9]
                    if bcrypt.checkpw(pin_to_check, hashed_pin_from_db):
                   # if pin2 == result[0][9]:
                       # z2=result[0][8]
                        print_green("Your balance is: ")
                        print(result[0][3],'\n\n')
                    else:
                        print_red("Incorrect PIN\n\n")
                        time.sleep(3)
                        run_program()
                else:
                    print_red("Incorrect Account Number\n\n")  
                    time.sleep(3)
                    run_program()          
             
                # Add code here to check the account balance
            elif user_selection ==5:
                acno = input("Enter your account number: ")
    
                 # Execute a query to search for the account number
                query = "SELECT * FROM bankdatas WHERE acno = %s"
                cur.execute(query, [acno])
    
    # Fetch the result
                result = cur.fetchall()
    
    # If account number is found
                if result:
        # Take PIN as input
                    #pin1 = int(input("Enter your PIN: "))
                    pin_to_check = input("Enter your PIN: ").encode('utf-8')
                    hashed_pin_from_db = result[0][9] 
        # Check if the PIN is correct
                    #if pin1 == result[0][8]:
                    if bcrypt.checkpw(pin_to_check, hashed_pin_from_db):  # assuming PIN is stored in the 8th column
            # Print all details of the person
                        print("Account Details:"             )
                        print("Account Number:", result[0][2])
                        print("Name:", result[0][1]          )
                        print("Address:", result[0][5]      )
                        print("Balance:", result[0][3]       )
                        # result=cur.fetchall()
                        current_balance = result[0][3]
                        deposit_amount = float(input("Enter the amount to deposit: "))
                        if(deposit_amount<=0):
                            print_red("Invalid Amount\n\n")
                            time.sleep(3)
                            run_program()

                     # Update the balance in the database
                        new_balance = current_balance + deposit_amount
                        query = "UPDATE bankdatas SET Deposit = %s WHERE acno = %s"
                        cur.execute(query, (new_balance, acno))
                      # Commit the changes
                        
                        print_green("Deposit successful!")
                        print('New balance:',new_balance)
                        conn.commit()
                    else:
                        print_red("Incorrect PIN\n\n")
                        time.sleep(3)
                        run_program    
                # main_menu()
            
            elif user_selection==6 :
               
                transferMoney()
                             
            elif user_selection == 7:
                print_red('Thank you for visiting GreenLand Bank. Goodbye!')
                break
            else:
                invalid_selection()
        except ValueError:
            invalid_selection()

if __name__ == '__main__':
    run_program()



