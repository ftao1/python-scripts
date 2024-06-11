# Quick python script to remove whitespace in filenames for the current dir
# v.01
# By F.Tao
#
# 7 Jun 2022
#

import os
import re

for file in os.listdir("."):
    new = re.sub(r"\s+", "_", file)
    os.rename(file, new)

