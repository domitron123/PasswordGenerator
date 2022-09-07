from os import stat
from pickle import APPEND
from random import choices, random
from tkinter.tix import ButtonBox
import easygui
import string
import random
import hashlib
from cryptography.fernet import Fernet
import atexit
import os


# * lists for generated password and list including all characters
passwd = []
characters = string.ascii_letters + string.digits + string.punctuation

full = 'storage.txt'

#ANCHOR
def my_exit_function(Program_ended):

    # * open file in read mode
    file = open("storage.txt", "r")

    # * read the content of file
    Len = file.read().replace(" ", "")

    # * get the length of the data
    ChaLen = len(Len)

    # * if storage.txt file is != 0 bytes and if the character length is <= 99
    # * this is to prevent an encrypted password become encrypted
    if os.stat(full).st_size != 0 and ChaLen <= 99:
        print("File is filled")

        # * opening the key
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()

        # * using the generated key
        fernet = Fernet(key)

        # * opening the original file to encrypt
        with open('storage.txt', 'rb') as file:
            original = file.read()

        # * encrypting the file
        encrypted = fernet.encrypt(original)

        # * opening the file in write mode and
        # * writing the encrypted data
        with open('storage.txt', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        print("'storage.txt' encrypted")

#ANCHOR
if __name__ == '__main__':
    # * if script ends then run encryption above
    atexit.register(my_exit_function, 'some argument', )

    #ANCHOR #& StartUp function which launches login screen and encrypts storage.txt
    def StartUp():

        enteracc = easygui.buttonbox(
            "Password generator - Dom", choices=("Login", "Create account"))
        # todo PASSWORD SAVING AMONG LINES
        if enteracc == "Login":
            login()
            
        #* will warn that creating new account will erase already saved passwords if there are bytes saved within 'storage.txt' 
        #& this eliminates the issue of a user creating a new account and viewing saved passwords
        if enteracc == "Create account" and os.stat(full).st_size != 0:
                erase = easygui.buttonbox(
                    "WARNING: CREATING A NEW ACCOUNT WILL EREASE ALL CURRENT SAVED PASSWORDS", choices=("Continue", "Go back"))
                if erase == "Go back":
                    login()
                if erase == "Continue":
                    #* erases all characters within 'stroage.txt' file
                    open("storage.txt", "w").close()
                    signup()
        if enteracc == "Create account" and os.stat(full).st_size == 0:
            signup()
        else:
            SystemExit()

    # ANCHOR #& signup function - create user account
    def signup():
        
            email = easygui.enterbox("Enter email address: ")
            userpw = easygui.passwordbox("Enter password: ")
            conf_userpw = easygui.passwordbox("Confirm password: ")

            if conf_userpw == userpw:
                # * encode the users password
                enc = conf_userpw.encode()
                hash1 = hashlib.md5(enc).hexdigest()

            else:
                easygui.msgbox("Password is not same as above! \n")
                signup()

            # * create 'credentials.txt' file and save the users email and encoded password within
            with open("credentials.txt", "w") as f:
                f.write(email + "\n")
                f.write(hash1)
            f.close()
            easygui.msgbox("You have registered successfully!")
            login()
    #ANCHOR #& login function - login window
    def login():
        email = easygui.enterbox("Enter email: ")
        userpw = easygui.passwordbox("Enter password: ")

        # *  verifies that users password matches encoded password in 'credentials.txt'
        auth = userpw.encode()
        auth_hash = hashlib.md5(auth).hexdigest()
        with open("credentials.txt", "r") as f:
            stored_email, stored_pwd = f.read().split("\n")
        f.close()

        if email == stored_email and auth_hash == stored_pwd:

            if os.stat(full).st_size != 0:

                # * opening the key
                with open('filekey.key', 'rb') as filekey:
                    key = filekey.read()

                # * using the key
                fernet = Fernet(key)

                # * opening the encrypted file
                with open('storage.txt', 'rb') as enc_file:
                    encrypted = enc_file.read()

                # * decrypting the file
                decrypted = fernet.decrypt(encrypted)

                # * opening the file in write mode and
                # * writing the decrypted data
                with open('storage.txt', 'wb') as dec_file:
                    dec_file.write(decrypted)

            print("'storage.txt' unencrypted")

            easygui.msgbox("Logged in Successfully!")
            Main()

        else:
            easygui.msgbox("Login failed! \n")
            login()

    #ANCHOR #& Main function interface menu - view existing passwords or generate new
    def Main():
        MainChoice = easygui.buttonbox("Password generator", choices=(
            "Create new password", "View existing passwords"))
        if MainChoice == "Create new password":
            GeneratePwd()
        if MainChoice == "View existing passwords":
            # todo WORK ON SAVED PASSWORDS AMONG MULTIPLE LINES
            easygui.msgbox("Password view in progress")
            Main()
        else:
            quit()

    #ANCHOR #& GeneratePwd function - generates users password and saves in 'storage.txt'
    def GeneratePwd():
        ChaLen = easygui.integerbox("How many characters")
        # * generate password length depending on ChaLen length
        for i in range(ChaLen):
            # * joins random items from character list and randomises final password - new user password is saved as 'passwd'
            passwd = ''.join(random.choice(characters) for i in range(ChaLen))

        # * opens 'storage.txt' file and writes newly generated password
        file = open('storage.txt', 'a')
        file.write(passwd)
        file.write('\n')
        # * closes file to save
        file.close()
        easygui.msgbox("Your generated password is: " + passwd)
        Main()

    #ANCHOR #& initialize StartUp function
    StartUp()