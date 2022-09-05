from asyncore import write
import easygui

modified = []


def AddToStorage():
    passwdEntry = easygui.enterbox("password:")
    file = open('storage.txt', 'w')
    file.write('\n')
    file.write(passwdEntry + '\n')
    file.close()
    AddToStorage()

#* GetPwed function reads certain line from .txt file 
def GetPwd():
    #* open the file and save the written context in 'read'
    file = open('storage.txt', 'r')
    read = file.readlines()
    file.close()
    
    #* for each line - strip the lines taking away the \n
    for line in read:
        modified.append(line.strip())

    #* print desired line 
    print(modified)



#* call function
AddToStorage()

#* call function
GetPwd()