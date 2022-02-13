import os
import shutil
from rich import print

# TODO: Nicer terminal interface
#       Device detection and selection
#       Copying files instead of moving
#       Entries less than 1000 do not work

def copyPartFiles(partNumber, newDirectory):
    rootDir = "Fake Gcode"
    fileName = f"cgip{partNumber}"
    folderName = f"{int(int(partNumber)/1000)}000s"
    partDir = (f"{rootDir}/{folderName}/{fileName}.nc")


    print(f"Checking: {partDir}")
    filesToCopy = []
    if os.path.isfile(partDir) == True:
        filesToCopy.append(partDir)
        print("File found")
        
        for i in range(9):
            print(f"{partDir[:-3]}-{i+1}.nc")
            if os.path.isfile(f"{partDir[:-3]}-{i+1}.nc") == True:
                filesToCopy.append(f"{partDir[:-3]}-{i+1}.nc")
            else:
                print(f"Found {i+1} OPs")
                break
        print(filesToCopy)
    else:
        print("No files found!")

    for j in filesToCopy:
        newFileName = j.split('/')[2]
        shutil.move(j,f"Fake USB/{newFileName}")
        print(f"Moved file: {newFileName}!")

while True:
    partNumber = "Not a number"
    while partNumber.isnumeric() == False:
        partNumber = input("Enter a part number:")
    copyPartFiles(partNumber,False)