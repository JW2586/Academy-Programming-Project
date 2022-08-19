from curses.ascii import isspace
from importlib.metadata import files
import tkinter
from tkinter import BOTH, END, LEFT
import ftplib
import os
import re
import csv
from datetime import date
ftp = ftplib.FTP()

def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def printFile():
    for row in data:
        print(row)


def checkHeaders(valid):
    headerTemplate = ['batch_id', 'timestamp', 'reading1', 'reading2', 'reading3', 'reading4', 'reading5', 'reading6',
                      'reading7', 'reading8', 'reading9', 'reading10']
    if data[0] != headerTemplate:
        valid = False
    
    return valid
        # data[0] = headerTemplate

def checkBatchIDDuplicates(valid):
    batchIDs = []
    for row in range(1, len(data)):
        if data[row][0] in batchIDs:
            # print("duplicate")
            valid = False
            # print("INVALID FILE")
            
        else:
            batchIDs.append(data[row][0])

        return valid

def checkValues(valid):
    # print("IS IT VALID: ",valid)
    for row in data:
        for item in row:
            if len(item) == 0 or item.isspace():
                # print("empty item")
                # print("INVALID FILE")
                valid = False
            else:
                if item.isdigit():
                    bob = 0
                    # print("number")
                elif item.isalnum():
                    bob = 0
                    # print("string")
                elif isFloat(item):
                    bob = 0
                    # print("float")
                    if float(item) >= 10:
                        # print("EXCEED")
                        # print(item)
                        valid = False
                        # print("INVALID FILE")
                        ##SCRAP FILE##
                    elif(format(float(item),".3f") != item):  #Check if 3dp
                        # print(float(item))
                        # print("NOT 3dp")
                        valid = False
                        # print("INVALID FILE")

    return valid

def checkMalformed(valid):
    for row in data:
        rowItemCounter = 0  ## Count items in row
        for item in row:
            rowItemCounter = rowItemCounter + 1;
        if(rowItemCounter != 12):  #Not enough colunms for correct format!
            # print("File malformed")
            valid = False
            # print("INVALID FILE")
            ## scrap file
    return valid

def connectServer():
    ip = "127.0.0.1"
    port = 21
    try:
        msg = ftp.connect(ip,port)
        print(msg)
        loginServer()
        # text_servermsg.insert(END,"\n")
        # text_servermsg.insert(END,msg)
        # lbl_login.place(x=150,y=20)
        # ent_login.place(x=150,y=43)
        # lbl_pass.place(x=150,y=70)
        # ent_pass.place(x=150,y=93)
        # btn_login.place(x=182,y=120)
    except:
        # text_servermsg.insert(END,"\n")
        # text_servermsg.insert(END,"Unable to connect")
        print("Unable to connect")

def loginServer():
    user = "user"
    password = "12345"
    try:
        msg = ftp.login(user,password)
        print(msg)
        downloadFile()
        # text_servermsg.insert(END,"\n")
        # text_servermsg.insert(END,msg)
        # year_lbl.place(x=280,y=20)
        # year_input.place(x=280,y=43)
        # month_lbl.place(x=280,y=70)
        # month_input.place(x=280,y=93)
        # date_lbl.place(x=280,y=120)
        # date_input.place(x=280,y=143)
        # btn_downfile.place(x=280,y=170)
        # btn_disconnect.place(x=150,y=585)
        # btn_exit.place(x=280,y=585)
    except Exception as e:
        print("ERROR: ", e)
        # text_servermsg.insert(END,"\n")
        # text_servermsg.insert(END,"Unable to login")
        print("Unable to login")
    
def downloadFile():
    canDownload = True
    # year = str(date.today().year)
    # month = str(date.today().month)
    # day = str(date.today().day)
    # year = year_input.get()
    # month = month_input.get()
    # date = date_input.get()

    # if len(year) == 0 or year.isspace():
    #     text_servermsg.insert(END,"\n")
    #     text_servermsg.insert(END,"Year cannot be empty")
    #     canDownload = False
    # if len(month) == 0 or month.isspace():
    #     text_servermsg.insert(END,"\n")
    #     text_servermsg.insert(END,"Month cannot be empty")
    #     canDownload = False
    # if len(date) == 0 or date.isspace():
    #     text_servermsg.insert(END,"\n")
    #     text_servermsg.insert(END,"Date cannot be empty")
    #     canDownload = False
    if canDownload == True:
        filesFound = 0
        formattedDate = date.today().strftime('%Y%m%d')
        print("Date: "+formattedDate)
        # print("FORMATTED DATE: "+formattedDate)
        ftp.cwd('/ftpserver/ftpFiles')
        # print(ftp.pwd())
        os.chdir('temp-downloads')
        for filename in ftp.nlst():
            # print(filename)
            if re.search("MED_DATA_"+formattedDate+"[0-9]{6}.csv", filename):
                # print("MATCH!!!!")
                filesFound += 1
                # text_servermsg.insert(END,"\n")
                # text_servermsg.insert(END,"Downloading " + filename)
                print("Downloading " + filename)
                
                with open(filename, 'wb') as file_handle:
                    try:
                        ftp.retrbinary("RETR " + filename, file_handle.write)
                        # print("finished")
                    except:
                        # text_servermsg.insert(END,"\n")
                        # text_servermsg.insert(END,"Unable to download file")   
                        print("Unable to download file")                     
        
        if filesFound > 0:
            # text_servermsg.insert(END,"\n")
            # text_servermsg.insert(END,"Downloaded "+str(filesFound)+" files")
            print("Downloaded "+str(filesFound)+" files")
            # text_servermsg.insert(END,"\n")
            # text_servermsg.insert(END,"Files from requested date downloaded")
            print("Files from requested date downloaded")
            # btn_validate.place(x=280,y=200)
            os.chdir('..')
            validateFile()
        else:
            # text_servermsg.insert(END,"\n")
            # text_servermsg.insert(END,"That file doesn't exist!")
            print("That file doesn't exist!")
            os.chdir('..')


                
    else:
        # text_servermsg.insert(END,"\n")
        # text_servermsg.insert(END,"You must enter a date!")
        print("You must enter a date!")
    
def validateFile():
    # year = str(date.today().year)
    # month = str(date.today().month)
    # day = str(date.today().day)
    # year = year_input.get()
    # month = month_input.get()
    # date = date_input.get()
    # formattedDate = year+month+day
    
    # text_servermsg.insert(END,"\n")
    # text_servermsg.insert(END,"Validating files...")
    print("Validating files...")
    directory = "temp-downloads"
    filesValidated = 0
    for filename in os.listdir(directory):
        valid = True
        # print(filename)
        openFile = open("temp-downloads/"+filename, "rt")
        global data
        data = list(csv.reader(openFile))
        openFile.close()
        # VALIDATION
        # printFile()
        valid = checkHeaders(valid)
        valid = checkBatchIDDuplicates(valid)
        valid = checkValues(valid)
        valid = checkMalformed(valid)
        filesValidated += 1
        if valid == False:
            # text_servermsg.insert(END,"\n")
            # text_servermsg.insert(END,filename+": FILE INVALID")
            print(filename+": FILE INVALID")
            os.remove("temp-downloads/"+filename)
            # text_servermsg.insert(END,"\n")
            # text_servermsg.insert(END,filename+": FILE DELETED")
        else:
            # text_servermsg.insert(END,"\n")
            # text_servermsg.insert(END,filename+": FILE VALID")
            print(filename+": FILE VALID")
            # fileDate = year+"/"+month+"/"+day
            fileDate = date.today().strftime('%Y/%m/%d')
            print("Date path: "+fileDate)
            newpath = "validated-files/"+fileDate
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            os.replace(os.path.join("temp-downloads", filename), os.path.join(newpath, filename))
            # text_servermsg.insert(END,"\n")
            # text_servermsg.insert(END,filename+": FILE SAVED")

    if filesValidated > 0:
        # text_servermsg.insert(END,"\n")
        # text_servermsg.insert(END,"Checked "+str(filesValidated)+" files")
        print("Checked "+str(filesValidated)+" files")
    else:
        # text_servermsg.insert(END,"\n")
        # text_servermsg.insert(END,"No files downloaded")
        print("No files downloaded")
        # text_servermsg.insert(END,"\n")
        # text_servermsg.insert(END,"You must download files before validating")
        print("You must download files before validating")

def closeConnection():
    try:
        # text_servermsg.insert(END,"\n")
        # text_servermsg.insert(END,"Closing connection...")
        print("Closing connection...")
        # text_servermsg.insert(END,"\n")
        # text_servermsg.insert(END,ftp.quit())
        print(ftp.quit())
    except:
        # text_servermsg.insert(END,"\n")
        # text_servermsg.insert(END,"Unable to disconnect")
        print("Unable to disconnect")

def exit():
    quit()

connectServer()