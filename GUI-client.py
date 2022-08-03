# Author: Jake W

from curses.ascii import isspace
from importlib.metadata import files
import tkinter
from tkinter import BOTH, END, LEFT
import ftplib
import os
import re
import csv
ftp = ftplib.FTP()

def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def checkHeaders(valid):
    headerTemplate = ['batch_id', 'timestamp', 'reading1', 'reading2', 'reading3', 'reading4', 'reading5', 'reading6',
                      'reading7', 'reading8', 'reading9', 'reading10']
    if data[0] != headerTemplate:
        valid = False
    
    return valid

def checkBatchIDDuplicates(valid):
    batchIDs = []
    for row in range(1, len(data)):
        if data[row][0] in batchIDs:
            valid = False
        else:
            batchIDs.append(data[row][0])

    return valid

def checkValues(valid):
    for row in data:
        for item in row:
            if len(item) == 0 or item.isspace():
                valid = False
            else:
                if isFloat(item) and not item.isdigit() and not item.isalnum():
                    if float(item) >= 10:
                        valid = False
                    elif(format(float(item),".3f") != item):  # Check if 3dp
                        valid = False

    return valid

def checkMalformed(valid):
    for row in data:
        rowItemCounter = 0  # Count items in row
        for item in row:
            rowItemCounter = rowItemCounter + 1
        if(rowItemCounter != 12):  # Not enough columns for correct format!
            valid = False

    return valid

def connectServer():
    ip = ent_ip.get()
    port = int(ent_port.get())
    try:
        msg = ftp.connect(ip,port)
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,msg)
        lbl_login.place(x=150,y=20)
        ent_login.place(x=150,y=43)
        lbl_pass.place(x=150,y=70)
        ent_pass.place(x=150,y=93)
        btn_login.place(x=182,y=120)
    except:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to connect")

def loginServer():
    user = ent_login.get()
    password = ent_pass.get()
    try:
        msg = ftp.login(user,password)
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,msg)
        year_lbl.place(x=280,y=20)
        year_input.place(x=280,y=43)
        month_lbl.place(x=280,y=70)
        month_input.place(x=280,y=93)
        date_lbl.place(x=280,y=120)
        date_input.place(x=280,y=143)
        btn_downfile.place(x=280,y=170)
        btn_disconnect.place(x=150,y=585)
        btn_exit.place(x=280,y=585)
    except Exception as e:
        print("ERROR: ", e)
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to login")
    
def downloadFile():
    canDownload = True
    year = year_input.get()
    month = month_input.get()
    date = date_input.get()
    if len(year) == 0 or year.isspace():
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Year cannot be empty")
        canDownload = False
    if len(month) == 0 or month.isspace():
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Month cannot be empty")
        canDownload = False
    if len(date) == 0 or date.isspace():
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Date cannot be empty")
        canDownload = False
    if canDownload == True:
        filesFound = 0
        formattedDate = year+month+date
        ftp.cwd('/ftpserver/ftpFiles')
        if not os.path.exists('temp-downloads'):
                os.mkdir('temp-downloads')
        os.chdir('temp-downloads')
        for filename in ftp.nlst():
            if re.search("MED_DATA_"+formattedDate+"[0-9]{6}.csv", filename):
                filesFound += 1
                text_servermsg.insert(END,"\n")
                text_servermsg.insert(END,"Downloading " + filename)
                
                with open(filename, 'wb') as file_handle:
                    try:
                        ftp.retrbinary("RETR " + filename, file_handle.write)
                    except:
                        text_servermsg.insert(END,"\n")
                        text_servermsg.insert(END,"Unable to download file")                        
        
        if filesFound > 0:
            text_servermsg.insert(END,"\n")
            text_servermsg.insert(END,"Downloaded "+str(filesFound)+" files")
            text_servermsg.insert(END,"\n")
            text_servermsg.insert(END,"Files from requested date downloaded")
            btn_validate.place(x=280,y=200)
            os.chdir('..')
        else:
            text_servermsg.insert(END,"\n")
            text_servermsg.insert(END,"That file doesn't exist!")
            os.chdir('..')


                
    else:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"You must enter a date!")
    
def validateFile():
    year = year_input.get()
    month = month_input.get()
    date = date_input.get()
    text_servermsg.insert(END,"\n")
    text_servermsg.insert(END,"Validating files...")
    directory = "temp-downloads"
    if not os.path.exists('temp-downloads'):
                os.mkdir('temp-downloads')
    filesValidated = 0
    for filename in os.listdir(directory):
        valid = True
        openFile = open("temp-downloads/"+filename, "rt")
        global data
        data = list(csv.reader(openFile))
        openFile.close()

        # VALIDATION
        valid = checkHeaders(valid)
        valid = checkBatchIDDuplicates(valid)
        valid = checkValues(valid)
        valid = checkMalformed(valid)
        filesValidated += 1
        if valid == False:
            text_servermsg.insert(END,"\n")
            text_servermsg.insert(END,filename+": FILE INVALID")
            os.remove("temp-downloads/"+filename)
        else:
            text_servermsg.insert(END,"\n")
            text_servermsg.insert(END,filename+": FILE VALID")
            fileDate = year+"/"+month+"/"+date
            newpath = "validated-files/"+fileDate
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            os.replace(os.path.join("temp-downloads", filename), os.path.join(newpath, filename))

    if filesValidated > 0:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Checked "+str(filesValidated)+" files")
    else:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"No files downloaded")
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"You must download files before validating")

def closeConnection():
    try:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Closing connection...")
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,ftp.quit())
    except:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to disconnect")

def exit():
    quit()

window = tkinter.Tk()
window.title("FTP Client")
window.wm_iconbitmap("favicon.ico")
window.geometry("420x620")
window.configure(bg='#2e2e2e')

#Buttons to connect to FTP cerver
lbl_ip = tkinter.Label(window, text="IP Address")
ent_ip = tkinter.Entry(window)
lbl_port = tkinter.Label(window, text="Port")
ent_port = tkinter.Entry(window)
btn_connect = tkinter.Button(window, text="Connect", command=connectServer)

#Output commands from server
text_servermsg = tkinter.Text(window,width=47,height=20)

#Buttons for logging in
lbl_login = tkinter.Label(window, text="Username")
ent_login = tkinter.Entry(window)
lbl_pass = tkinter.Label(window, text="Password")
ent_pass = tkinter.Entry(window)
btn_login = tkinter.Button(window, text="Login", command=loginServer)

#Inputs
year_input = tkinter.Entry(window)
year_lbl = tkinter.Label(window, text="Year:")
month_input = tkinter.Entry(window)
month_lbl = tkinter.Label(window, text="Month:")
date_input = tkinter.Entry(window)
date_lbl = tkinter.Label(window, text="Date:")

#File handling buttons
btn_downfile = tkinter.Button(window, text="Download Files", command=downloadFile,width=15)
btn_validate = tkinter.Button(window, text="Validate Files", command=validateFile,width=15)

#Quit buttons
btn_disconnect = tkinter.Button(window, text="Disconnect", command=closeConnection,width=15)
btn_exit = tkinter.Button(window, text="Exit", command=exit,width=15)

#Place default widgets
lbl_ip.place(x=20,y=20)
ent_ip.place(x=20,y=43)
lbl_port.place(x=20,y=70)
ent_port.place(x=20,y=93)
btn_connect.place(x=52,y=120)
text_servermsg.place(x=20,y=250)

#Create
window.mainloop()
