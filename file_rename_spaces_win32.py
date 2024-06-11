# Quick script for win32 systems to rename filenames that contain spaces to _
# v.0.1
#
# By F.TAO
#
# 7th June 2022
#

import os
import re
from easygui import diropenbox

os.system('cls')
print("Please select the folder containing files to rename in the dialogue box:\n")

userpath = diropenbox("Folder Selection", "Choose folder containing files to rename:")
os.chdir(userpath)

for file in os.listdir(userpath):
    new = re.sub(r"\s+", "_", file)
    os.rename(file,new)
    print(new)

print("\nRenaming complete.\n")

