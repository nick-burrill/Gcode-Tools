import os
import shutil
from rich import print

# TODO: Nicer terminal interface
#       Device detection and selection
#       Copying files instead of moving
#       Entries less than 1000 do not work

partNumber = input("Enter a part number:")
rootDir = "Fake Gcode"

fileName = f"cgip{partNumber}"
folderName = f"{partNumber[0]}000"
partDir = (f"{rootDir}/{folderName}/{fileName}.nc")

print(f"Checking: {partDir}")
files = []
if os.path.isfile(f"{rootDir}/{folderName}/{fileName}.nc") == True:
    files.append(f"{rootDir}/{folderName}/{fileName}.nc")
    print("File found")
    for i in range(10):
        if os.path.isfile(f"{rootDir}/{folderName}/{fileName}-{i+1}.nc") == True:
            files.append(f"{rootDir}/{folderName}/{fileName}-{i+1}.nc")
        else:
            print(f"Found {i+1} OPs")
            break
    print(files)
else:
    print("No files found!")

for j in files:
    newFileName = j[16:] # Jank af
    print(f"Moved file: {newFileName}!")
    shutil.move(j,f"Fake USB/{newFileName}")