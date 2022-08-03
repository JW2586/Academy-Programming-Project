# Author: Sam M1

from fileinput import filename
import ftplib
import os
import re
import csv
ftp = ftplib.FTP()

def main():  # Main menu (Start program or quit)
    while(True):
        print("__MENU__")
        print("1) Start")
        print("2) Quit")
        userInput = int(input("Please enter 1 or 2 respectivly..\n"))
        if(userInput == 1):
            clientMethod()
        else:
            closeConnection()
            quit(0)

def clientMethod():  # Where most of the work is done
    ipAddress = getIP()
    portNumber = getPort()
    connectToServer(portNumber, ipAddress)
    username = getUname()
    password = getPword()
    loginServer(username,password)
    print("Commands include: 'ls','cd','mkdir','rmdir','rmfile','dlfile','upfile'")
    while(True):  # Keeps you on the ftp cli
        consoleCommands = input("ftpCMD@" + username + ": ")
        if(consoleCommands == "ls"):
            displayDir()
        elif(consoleCommands == "cd"):
            dirName = input("Please enter the name of the directory\n")
            changeDirectory(dirName)
        elif(consoleCommands == "mkdir"):
            dirName = input("Please enter the name of the directory\n")
            createDirectory(dirName)
        elif (consoleCommands == "rmdir"):
            dirName = input("Please enter the name of the directory\n")
            deleteDirectory(dirName)
        elif (consoleCommands == "rmfile"):
            fileName = input("Please enter the name of the file\n")
            deleteFile(fileName)
        elif (consoleCommands == "dlfile"):
            downloadFile()
        elif (consoleCommands == "upfile"):
            fileName = input("Please enter the name of the file")
            uploadFile(fileName)

## Directory Methods ##
def displayDir():  # Displays all the current files in the location of the ftp server
    print("-------------------------------------")
    dirlist = []
    dirlist = ftp.nlst()
    for item in dirlist:
        print(item)
    print("-------------------------------------")

def changeDirectory(directory):  # Change current directory
    try:
        msg = ftp.cwd(directory)
        print(msg)
    except:
        print("Unable to change directory")
    displayDir()

def createDirectory(directory):  # Creats a new directory
    try:
        msg = ftp.mkd(directory)
        print(msg)
    except:
        print("Unable to make directory")
    displayDir()

def deleteDirectory(directory):  # Deletes a directory
    try:
        msg = ftp.rmd(directory)
        print(msg)
    except:
        print("Unable to remove directory")
    displayDir()

## File Methods ##
def deleteFile(fileName): # Deletes a singular file
    try:
        msg = ftp.delete(fileName)
        print(msg)
    except:
        print("Unable to delete file")

def downloadFile():  # Downloads files from selected date and calls validation method
    canDownload = True
    year = getYear()
    month = getMonth()
    date = getDay()
    if len(year) == 0 or year.isspace():
        print("Year cannot be empty")
        canDownload = False
    if len(month) == 0 or month.isspace():
        print("Month cannot be empty")
        canDownload = False
    if len(date) == 0 or date.isspace():
        print("Date cannot be empty")
        canDownload = False
    if canDownload == True:
        filesFound = 0
        formattedDate = year + month + date
        ftp.cwd('/ftpserver/ftpFiles')
        if not os.path.exists('temp-downloads'):
                os.mkdir('temp-downloads')
        os.chdir('temp-downloads')
        for filename in ftp.nlst():
            if re.search("MED_DATA_" + formattedDate + "[0-9]{6}.csv", filename):
                filesFound += 1
                print("Downloading " + filename)

                with open(filename, 'wb') as file_handle:
                    try:
                        ftp.retrbinary("RETR " + filename, file_handle.write)
                    except:
                        print("Unable to download file")

        if filesFound > 0:
            print("Downloaded "+str(filesFound)+" files")
            print("Files downloaded successfully")
            os.chdir('..')
            validateFile(year,month,date)
        else:
            print("That file does not exist")
            os.chdir('..')
    else:
        print("You must enter a date")

def uploadFile(fileName):
    try:
        up = open(fileName, "rb")
        print("Uploading " + fileName)
        ftp.storbinary("STOR " + fileName, up)
    except:
        print("Unable to upload file")


## Connecting Methods (Connect, login and disconnect) ##
def connectToServer(port, ipAddy):  # Makes connection to ftp server
    try:
        msg = ftp.connect(ipAddy, port)
        print(msg)
        print("Connected")
    except:
        print("Unable to connect")
        quit(1)

def loginServer(userName, passWord):  # Gets logins and sends to ftp
    try:
        msg = ftp.login(userName,passWord)
        print(msg)
        print("Logged in")
    except:
        print("Unable to Login")
        quit(1)

def closeConnection():  # Ends the ftp connection
    try:
        print("Closing connection...")
        ftp.quit()
    except:
        print("Unable to disconnect")

## File Validation ##
def validateFile(yearInp,monthInp,dayInp): # Runs all the various validation methods
    year = yearInp
    month = monthInp
    date = dayInp
    print("Validating files...")
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
            print(filename+": FILE INVALID")
            os.remove("temp-downloads/"+filename)
        else:
            print(filename+": FILE VALID")
            fileDate = year+"/"+month+"/"+date
            newpath = "validated-files/"+fileDate
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            os.replace(os.path.join("temp-downloads", filename), os.path.join(newpath, filename))
            
    if filesValidated > 0:
        print("Checked "+str(filesValidated)+" files")
    else:
        print("No files downloaded")
        print("You must download files before validating")

def isFloat(num):  # Checks a variable is a float
    try:
        float(num)
        return True
    except ValueError:
        return False

def checkHeaders(valid):  # Replaces header of csv file
    headerTemplate = ['batch_id', 'timestamp', 'reading1', 'reading2', 'reading3', 'reading4', 'reading5', 'reading6',
                      'reading7', 'reading8', 'reading9', 'reading10']
    if data[0] != headerTemplate:
        valid = False

    return valid

def checkBatchIDDuplicates(valid):  # Check for duplicate batch ID
    batchIDs = []
    for row in range(1, len(data)):
        if data[row][0] in batchIDs:
            valid = False

        else:
            batchIDs.append(data[row][0])

        return valid


def checkValues(valid):  # Make sure values are valid ints of 3dp

    for row in data:
        for item in row:
            if len(item) == 0 or item.isspace():
                valid = False
            else:
                if isFloat(item) and not item.isdigit() and not item.isalnum():
                    if float(item) >= 10:
                        valid = False
                    elif (format(float(item), ".3f") != item):  # Check if 3dp
                        valid = False
    return valid


def checkMalformed(valid):  # Chech if colunms are formatted
    for row in data:
        rowItemCounter = 0  ## Count items in row
        for item in row:
            rowItemCounter = rowItemCounter + 1
        if (rowItemCounter != 12):  # Not enough colunms for correct format!
            valid = False
    return valid


## accessors below ##

def getUname():  # Gets username and password
    userName = input("Please Enter Your Username\n")
    return userName

def getPword():
    passWord = input("Please enter your password\n")
    return passWord

def getIP():  # Gets IP from user
    ipInput = input("Please enter the servers IPv4 address\n")
    return ipInput

def getPort():  # Gets port from user
    portInput = int(input("Please enter the required port\n"))
    return portInput

def getYear():
    year = input("Enter the year : \n")
    return year

def getMonth():
    month = input("Enter the month : \n")
    return month

def getDay():
    day = input("Enter the day : \n")
    return day


main()
