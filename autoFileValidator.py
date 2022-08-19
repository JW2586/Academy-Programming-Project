# Author: Jake W

from curses.ascii import isspace
from importlib.metadata import files
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
                if isFloat(item):
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
    ip = "127.0.0.1"
    port = 21
    try:
        msg = ftp.connect(ip,port)
        print(msg)
        loginServer()
    except:
        print("Unable to connect")

def loginServer():
    user = "user"
    password = "12345"
    try:
        msg = ftp.login(user,password)
        print(msg)
        downloadFile()
    except Exception as e:
        print("ERROR: ", e)
        print("Unable to login")
    
def downloadFile():
    canDownload = True
    if canDownload == True:
        filesFound = 0
        formattedDate = date.today().strftime('%Y%m%d')
        print("Date: "+formattedDate)
        ftp.cwd('/ftpserver/ftpFiles')
        os.chdir('temp-downloads')
        for filename in ftp.nlst():
            if re.search("MED_DATA_"+formattedDate+"[0-9]{6}.csv", filename):
                filesFound += 1
                print("Downloading " + filename)
                
                with open(filename, 'wb') as file_handle:
                    try:
                        ftp.retrbinary("RETR " + filename, file_handle.write)
                    except:  
                        print("Unable to download file")                     
        
        if filesFound > 0:
            print("Downloaded "+str(filesFound)+" files")
            print("Files from requested date downloaded")
            os.chdir('..')
            validateFile()
        else:
            print("That file doesn't exist!")
            os.chdir('..')
                
    else:
        print("You must enter a date!")
    
def validateFile():
    print("Validating files...")
    directory = "temp-downloads"
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
            print(filename+": FILE INVALID")
            os.remove("temp-downloads/"+filename)
        else:
            print(filename+": FILE VALID")
            fileDate = date.today().strftime('%Y/%m/%d')
            print("Date path: "+fileDate)
            newpath = "validated-files/"+fileDate
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            os.replace(os.path.join("temp-downloads", filename), os.path.join(newpath, filename))

    if filesValidated > 0:
        print("Checked "+str(filesValidated)+" files")
    else:
        print("No files downloaded")
        print("You must download files before validating")

def closeConnection():
    try:
        print("Closing connection...")
        print(ftp.quit())
    except:
        print("Unable to disconnect")

def exit():
    quit()

connectServer()