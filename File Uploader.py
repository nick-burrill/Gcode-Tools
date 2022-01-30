import os
import shutil
from rich import print

# TODO: Nicer terminal interface
#       Device detection and selection
#       Copying files instead of moving

partNumber = input("Enter a part number:")

fileName = f"cgip{partNumber}"
folderName = f"{partNumber[0]}000"
partDir = (f"gcode/{folderName}/{fileName}.nc")

print(f"Checking: {partDir}")
files = []
if os.path.isfile(f"gcode/{folderName}/{fileName}.nc") == True:
    files.append(f"gcode/{folderName}/{fileName}.nc")
    print("File found")
    for i in range(10):
        if os.path.isfile(f"gcode/{folderName}/{fileName} -{i+1}.nc") == True:
            files.append(f"gcode/{folderName}/{fileName} -{i+1}.nc")
        else:
            print(f"Found {i+1} OPs")
            break
    print(files)
else:
    print("No files found!")

for j in files:
    newFileName = j[11:]
    print(f"Moved file: {newFileName}!")
    shutil.move(j,f"fakeUSB/{newFileName}")