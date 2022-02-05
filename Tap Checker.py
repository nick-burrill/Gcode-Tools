from rich import print

# TODO: Drag drop file loading
#       Load file by launching with arguments
#       Pitch calculation
#       Pretty output table

filePath = "Sample Gcode/Solidworks/CGIP11719.NC"

with open(filePath, 'r') as file:
    lines = file.readlines()

def readLine(line):
    codeList = ['G','M','T','S','F','X','Y','Z','H','D','N','R','P']
    newWord = ""
    wordList = []
    for i, char in enumerate(line):
        if char in codeList or char == "\n" or char == " ":
            if newWord != "" and newWord != " ":
                wordList.append(newWord)
            newWord = ""
        newWord += char
    return(wordList)

def readWords(words, values):
    for word in words:
        letter = word[0] # Separate key letter from value
        value = word[1:]

        if letter == 'F':
            if values["feed"] == False:
                values["feed"] = value
        elif letter == 'S':
            if values["rpm"]== False:
                values["rpm"] = value
        elif letter == 'T':
            if values["tool"] == False:
                values["tool"] = value
        # print((letter,value))
    return(values)

tappingCycleIndex = []
for lineIndex, line in enumerate(lines):
    if line.find("G84") != -1:
        tappingCycleIndex.append(lineIndex+1)

allValues = []

for i, tappingCycle in enumerate(tappingCycleIndex):
    valueDict = {"feed":False, "rpm":False, "tool":False}
    lineToRead = tappingCycle
    while False in valueDict.values():
        words = readLine(lines[lineToRead])
        readWords(words, valueDict)
        lineToRead -= 1
    allValues.append(valueDict)

print(allValues)