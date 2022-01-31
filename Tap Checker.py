from rich.console import Console
from rich.table import Table
from rich import print
from decimal import *
import os, sys

try:
    droppedFile = sys.argv[1:]
except IndexError:
    print("No file selected")

for p in droppedFile:
    with open("1001.nc", 'r') as file:
        lines = file.readlines()



# Determine if each tool change has a tapping cycle or not
rigidTappingIndexes = []
for lineIndex, line in enumerate(lines):
    if line.find("G84") != -1:
        rigidTappingIndexes.append(lineIndex+1)
        # print(lineIndex, line)
# print("rigid tapping indexes:", rigidTappingIndexes)


allData = []

for tappingCycle in rigidTappingIndexes:
    feedPerRev = False
    Feed = 0
    FeedFound = False
    RPM = 0
    RPMFound = False
    Tool = 0
    toolFound = False
    
    readLine = tappingCycle

    while lines[readLine].find("M06") == -1:
        # print(lines[readLine])
        readLine = readLine - 1

        if lines[readLine].find("G95") != -1:
            feedPerRev = True

        if lines[readLine].find("F") != -1 and FeedFound == False:
            Feed = lines[readLine][lines[readLine].index('F')+1:].strip()
            Feed = Decimal(Feed)
            FeedFound = True

        if lines[readLine].find("S") != -1 and RPMFound == False:
            RPM = lines[readLine][lines[readLine].index('S')+1:].strip()
            RPM = Decimal(RPM)
            RPMFound = True

        if lines[readLine].find("T") != -1 and toolFound == False:
            Tool = lines[readLine][lines[readLine].index('T')+1:].strip()
            Tool = Tool.replace("M06",'')
            Tool = int(Tool)
            toolFound = True

    # Pitch Calculation
    if feedPerRev == True:
        iPitch = Feed
        mPitch = Feed*25.4
    else:
        iPitch = RPM/Feed
        mPitch = Feed/RPM*Decimal("25.4")

    # Convert all data into strings for table printing later
    data = {"ToolNum": Tool,
            "RPM":str(RPM),
            "Feed":str(Feed),
            "Feed/Rev":feedPerRev,
            "Metric Pitch": str(mPitch),
            "Imperial Pitch": str(iPitch)}
    allData.append(data)


# Sort data
allData = sorted(allData, key= lambda i: i['ToolNum'])

# Print Results
console = Console()
table = Table(show_header=True)
table.add_column("Tool")
table.add_column("RPM")
table.add_column("Feed")
table.add_column("Metric Pitch")
table.add_column("Imperial Pitch")
for tool in allData:
    table.add_row(str(tool["ToolNum"]),tool["RPM"],tool["Feed"],tool["Metric Pitch"],tool["Imperial Pitch"])
console.print(table)

input("Press enter to quit...")
