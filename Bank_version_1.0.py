import termcolor
import os
from colorama import init, Fore, Back, Style
import random
import mysql.connector
conn = mysql.connector.connect(
    host='localhost',
    password='@Ritik2004',
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
        pin1 = int(input("Enter your PIN: "))
        
        # Check if the PIN is correct
        if pin1 == result[0][8]:  # type: ignore # assuming PIN is stored in the 6th column
            # Print all details of the person
            print_cyan("Account Login Succesfully\n")  
            print_green("Account Details:")
            print("Account Number:", result[0][1])
            print("Name          :", result[0][0])
            print("Address       :", result[0][4])
            print("Balance       :", result[0][2])
             
            
        else:
            print("Invalid PIN")
            #sfun()
            
    else:
        print("Account number not found")
        

    # Close the cursor and connection
    #cursor.close()
    #cnx.close()
# Functin to take info
def getinfo(): #option 1
    a2=random.randint(10000000,99999999)
    c1=int(input("Mobile number:"))
    print("OTP has been sent successfuly")
    d=int(input("--->"))
    a=input("Enter Your Name :")
    b=input("DOB dd-mm-yy    :")
    c=input("Permanent Address :")
    e=int(input("Adhar No :"))
    d=input("E-mail  :")
    f=int(input("Add Money :"))
    g=int(input("create 4 digit security pin\n--->"))
    print_green("\n                   Congratulations! Mr/Mrs " + a + " your account created sucessfully\n")
    print_green("Your account number is : " + str(a2))
    print_magenta("\nPress 1 to Genrate E-Passbook :")
    h=int(input("--->"))
    t=(a,a2,f,b,c,d,e,c1,g) 
    s="Insert into bankdatas(Name, Acno,Deposit,dob,Address,email,Adhar_no,Mobile,pin) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
    print_red('Invalid selection. Please try again.')

def main_menu():
    #display_advertisement()
    print_yellow('Please choose an option:')
    print(' ')
    print_cyan('1. Open a new account')
    print_cyan('2. Login')
    print_cyan('3. Withdraw funds')
    print_cyan('4. Check account balance')
    print_cyan('5. Deposit')
    print_red('6. Exit')
    print(' ')

def run_program():
   
    display_advertisement()
    
    while True:
        main_menu()
        try:
            user_selection = int(input('Enter your selection (1-5):\n--->'))
            if user_selection == 1:
                print_green('You selected: Open a new account')
                getinfo()
                # Add code here to open a new account
            elif user_selection == 2:
                print_cyan('You selected: Login ')
                login()
                #break
                #Add code here to process a deposit
                
            elif user_selection == 3:
                print_magenta('You selected: Withdraw funds')
                # Add code here to process a withdrawal
                print("This Service Availble in few days")
            elif user_selection == 4:
                print_yellow('You selected: Check account balance')
                print("This Service Availble in few days")
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
                    pin1 = int(input("Enter your PIN: "))
        
        # Check if the PIN is correct
                    if pin1 == result[0][8]:  # assuming PIN is stored in the 6th column
            # Print all details of the person
                        print("Account Details:"             )
                        print("Account Number:", result[0][1])
                        print("Name:", result[0][0]          )
                        print("Address:", result[0][4]      )
                        print("Balance:", result[0][2]       )
                        # result=cur.fetchall()
                        current_balance = result[0][2]
                        deposit_amount = float(input("Enter the amount to deposit: "))

                     # Update the balance in the database
                        new_balance = current_balance + deposit_amount
                        query = "UPDATE bankdatas SET Deposit = %s WHERE acno = %s"
                        cur.execute(query, (new_balance, acno))
                      # Commit the changes
                        
                        print_green("Deposit successful!")
                        print('New balance:',new_balance)
                        conn.commit()
                # main_menu()
            
             
            elif user_selection == 6:
                print_red('Thank you for visiting GreenLand Bank. Goodbye!')
                break
            else:
                invalid_selection()
        except ValueError:
            invalid_selection()

if __name__ == '__main__':
    run_program()




