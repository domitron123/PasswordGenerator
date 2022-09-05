from os import stat
from pickle import APPEND
from random import choices, random
import easygui
import string
import random
import hashlib


# * lists for generated password and list including all characters
passwd = []
characters = string.ascii_letters + string.digits + string.punctuation


# * StartUp function which launches login screen
def StartUp():
    enteracc = easygui.buttonbox(
        "Password generator - Dom", choices=("Login", "Create account"))
    # todo PASSWORD SAVING AND CREATING
    if enteracc == "Login":
        login()
    if enteracc == "Create account":
        signup()


#* signup function - create user account
def signup():
    email = easygui.enterbox("Enter email address: ")
    userpw = easygui.passwordbox("Enter password: ")
    conf_userpw = easygui.passwordbox("Confirm password: ")  

    if conf_userpw == userpw:
        #* encode the users password
         enc = conf_userpw.encode()
         hash1 = hashlib.md5(enc).hexdigest()     

    else:
        easygui.msgbox("Password is not same as above! \n")
        signup()

    #* create 'credentials.txt' file and save the users email and encoded password within
    with open("credentials.txt", "w") as f:
         f.write(email + "\n")
         f.write(hash1)
    f.close()
    easygui.msgbox("You have registered successfully!")  
    login()  


def login():
     email = easygui.enterbox("Enter email: ")
     userpw = easygui.passwordbox("Enter password: ")    

    #*  verifies that users password matches encoded password in 'credentials.txt'    
     auth = userpw.encode()
     auth_hash = hashlib.md5(auth).hexdigest()
     with open("credentials.txt", "r") as f:
         stored_email, stored_pwd = f.read().split("\n")
     f.close()     
     
     if email == stored_email and auth_hash == stored_pwd:
         easygui.msgbox("Logged in Successfully!")
         Main()
     else:
         easygui.msgbox("Login failed! \n")
         login()


# * Main function interface menu - view existing passwords or generate new
def Main():
    MainChoice = easygui.buttonbox("Password generator", choices=(
        "Create new password", "View existing passwords"))
    if MainChoice == "Create new password":
        GeneratePwd()
    if MainChoice == "View existing passwords":
        # todo WORK ON SAVED PASSWORDS
        easygui.msgbox("Password view in progress")
        Main()
    else:
        quit()


#* GeneratePwd function - generates users password and saves in 'storage.txt' 
#todo WORK IN PROGRESS - NEEDS TO BE MULTI-LINED('\N') AND ENCRYPTED
def GeneratePwd():
    ChaLen = easygui.integerbox("How many characters")
    #* generate password length depending on ChaLen length
    for i in range(ChaLen):
        #* joins random items from character list and randomises final password - new user password is saved as 'passwd'
        passwd = ''.join(random.choice(characters) for i in range(ChaLen))
        

    #* opens 'storage.txt' file and writes newly generated password
    file = open('storage.txt', 'w')
    file.write(passwd + '\n')
    #* closes file to save
    file.close()
    easygui.msgbox("Your generated password is: " + passwd)
    Main()

# * initialize StartUp function
StartUp()