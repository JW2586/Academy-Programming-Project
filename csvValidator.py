import csv

batchIDs = []

f = open("Samples - Invalid\Duplicate Batch Numbers\MED_DATA_20220803153918.csv", "rt")
##reader = csv.reader(f)
##for row in reader:
##    print(*row)

data = list(csv.reader(f))
f.close()


##print(data[0][0])

def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def printFile():
    for row in data:
        print(row)


def checkHeaders():
    print(data[0])
    headerTemplate = ['batch_id', 'timestamp', 'reading1', 'reading2', 'reading3', 'reading4', 'reading5', 'reading6',
                      'reading7', 'reading8', 'reading9', 'reading10']
    if data[0] == headerTemplate:
        print("VALID HEADERS")
    else:
        print("INVALID HEADERS")
        data[0] = headerTemplate


##        checkHeaders()

def checkBatchIDDuplicates():
    for row in range(1, len(data)):
        print(data[row][0])
        if data[row][0] in batchIDs:
            print("duplicate")
        else:
            batchIDs.append(data[row][0])


##            print(*batchIDs)

def checkValues():
    for row in data:
        for item in row:
            if len(year) == 0 or year.isspace():
                print("empty item")
            else:
                if item.isdigit():
                    bob = 0
                ##                    print("number")
                elif item.isalnum():
                    bob = 0
                ##                    print("string")
                elif isFloat(item):
                    bob = 0
                    ##                    print("float")
                    if float(item) > 9.9:
                        print("EXCEED")
                        print(item)
                        ##SCRAP FILE##

def checkRounded3DP():
    for row in data:
        for item in row:
            if len(year) == 0 or year.isspace():  # Check white space
                print("Empty")
            elif(format(item,".3f") == item):  #Check if 3dp
                print("item")
            else:
                print("Scrapping File")

def checkMalformed():
    for row in data:
        rowItemCounter = 0  ## Count items in row
        for item in row:
            rowItemCounter = rowItemCounter + 1;
        if(rowItemCounter != 12):  #Not enough colunms for correct format!
            print("File malformed")
            ## scrap file
        





