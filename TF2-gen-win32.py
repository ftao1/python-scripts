#!/usr/bin/env python
#
# Script        : TF2-gen-win.py
# Description   : Convert a MS Excel input file to a plain text file as terraform.tfvars file for Terraform. All info has been redacted.
# Dependencies  : python, pandas, easygui
# Usage         : python TF2-gen-win.py
# Author        : Fai Tao
# Version       : 0.1
# Date          : 15 Mar 2022
#
# Change history (most recent first)
#
# Date          Who             Comments
# ----          ---             --------
# 15/03/22      FT              Initial draft
#


import pandas as pd
import re
import shutil
import time
from os import system, remove
from easygui import fileopenbox

def welcome():

    system('cls')

    print("Welcome.\n\nThis script will help you create the 'terraform.tfvars' file.")
    print("The terraform.tfvars file contains the hardcoded values for VSphere such as DC name, network name, etc.\n")
    print("Please ensure the values are correct from the iDLD doc!\n")
    print("Please note that for DNS, if you have more that 1 DNS IP, each IP should be comma delimited.\n")


def openfile():
    # Open the Excel file as input. It is assumed that the input file is valid with correct values
    template = fileopenbox("Excel Template Selection", "Choose a Microsoft Excel (*.xlsx) template file:", filetypes=["*.xlsx"])

    df_excel = pd.read_excel(template)

    print(f"These are your entered values in MS Excel:\nTemplate Used: {template}\n\n {df_excel}")

    # Return the excel file as a plain text file for further processing
    return df_excel.to_csv('new.txt', header=None, sep='=', na_rep='NA', index=False)


def cleanup():
    # Cleanup the file produced by openfile
    today = time.strftime("%d %B %Y")

    with open("new.txt", "r") as readf, open("newtmp.txt", "w") as writef:
        # Write out header for the file
        writef.write(f"# terraform.tfvars\n# This file defines values for the variables declared in the variables.tf file.\n# Date: {today}\n\n")

        # Store regex patterns
        replacements = (
                    ("(dns_servers=)(\d.*)", "\\1[\"\\2\"]"),
                    ("\s*,\s*", "\", \""),
                    ("^(?!dns)(\w+=)(.*)", "\\1\"\\2\""),
        )

        content = readf.read()

        # Carry out regex operations on the file
        for pat, repl in replacements:
            content = re.sub(pat, repl, content,  0, re.MULTILINE)

        writef.write(content)
    # return the output of func
    return content


def output():
    # Copy .terratmp as terraform.tfvars
    shutil.copy("newtmp.txt", "terraform.tfvars")

    # Remove temp file .terratmp
    remove("newtmp.txt")

    # Get return value from cleanup() and assign to output var
    output = cleanup()

    # Print out further instructions for user
    print(f"\nThe file 'terraform.tfvars' has been created.\n\n{output}\nPlease check and copy to the terraform project directory.\n")

''' Call functions '''
welcome()
openfile()
cleanup()
output()


