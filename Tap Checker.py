from rich import print
from rich.console import Console
from rich.table import Table
from decimal import *
import sys

# TODO: Load file by launching with arguments
#       Pitch calculation for non feed/rev
#       Ignore comments when finding G84

manualFile=False
filePath = "Sample Gcode/Solidworks/CGIP11719.nc"

if manualFile == True:
    with open(filePath, 'r') as file:
        lines = file.readlines()
else:
    try:
        droppedFile = sys.argv[1:]
    except IndexError:
        print("No file selected")

    for p in droppedFile:
        filePath = p
        with open(p, 'r') as file:
            lines = file.readlines()

def readLine(line):
    codeList = ['G','M','T','S','F','X','Y','Z','H','D','N','R','P']
    newWord = ""
    wordList = []
    comment = False
    for i, char in enumerate(line):
        if char == "(":
            comment=True
        elif char == ")" and comment == True:
            comment=False

        elif char in codeList or char == "\n" or char == " ":
            if newWord != "" and newWord != " ":
                wordList.append(newWord)
            newWord = ""
        if comment==False and char != ")":
            newWord += char
    return(wordList)

def readWords(words, values):
    for word in words:
        letter = word[0] # Separate key letter from value
        value = word[1:]

        if letter == 'F':
            if values["feed"] == False:
                values["feed"] = float(value)
        elif letter == 'S':
            if values["rpm"]== False:
                values["rpm"] = int(value)
        elif letter == 'T':
            if values["tool"] == False:
                values["tool"] = int(value)
            if values["feedPerRev"] == False:
                values["feedPerRev"] = "NO"
        elif letter == 'G' and int(value) == 98:
            values["feedPerRev"] = True

        # print((letter,value))
    return(values)

tappingCycleIndex = [] # Store all G84 values to read related Gcode
for lineIndex, line in enumerate(lines):
    if line.find("G84") != -1:
        tappingCycleIndex.append(lineIndex+1)

allValues = [] # Store information about each tapping cycle

for tappingCycle in tappingCycleIndex:
    valueDict = {"tool":False, "rpm":False, "feed":False, "feedPerRev":False}
    lineToRead = tappingCycle
    while False in valueDict.values():
        words = readLine(lines[lineToRead])
        readWords(words, valueDict)
        lineToRead -= 1
    allValues.append(valueDict)

# Sort data
allValues = sorted(allValues, key= lambda i: i['tool'])

# Calculate pitches
def calculatePitch(tappingData):
    if tappingData["feedPerRev"] == True:
        tappingData["metricPitch"] = round(tappingData["feed"] * 25.4, 3)
        tappingData["threadsPerInch"] = round(1 / tappingData["feed"], 2)
    else:
        tappingData["metricPitch"] = round(tappingData["rpm"] / tappingData["feed"] * 25.4, 3)
        tappingData["threadsPerInch"] = round(tappingData["rpm"] / tappingData["feed"], 2)

for value in allValues:
    calculatePitch(value)

# Print Results
print("File loaded:", filePath)
console = Console()
table = Table(show_header=True)
table.add_column("Tool #")
table.add_column("RPM")
table.add_column("Feed")
table.add_column("Metric Pitch")
table.add_column("Threads per Inch")
for tool in allValues:
    table.add_row(str(tool["tool"]),str(tool["rpm"]),str(tool["feed"]),str(tool["metricPitch"]),str(tool["threadsPerInch"]))
console.print(table)


input("Press enter to continue...")