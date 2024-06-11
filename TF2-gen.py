#!/usr/bin/env python3

'''
DESC:
Python3 script to help create the terraform.tfvars input file that contains real values for the project.
Please ensure that the values are correct by checking the iDLD doc.
Terraform is a very powerful orchestration tool and can damage existing infrastructure if care is not taken to double check!
'''

__author__ = "Fai Tao"
__date__ = "14 Mar 2022"
__version__ = "0.4.0"
__license__ = "MIT"

import time
import shutil
import re
from os import system, remove

def welcome():

    system('clear')

    print("Welcome.\n\nThis script will help you create the terraform.tfvars file.")
    print("The terraform.tfvars file contains the hardcoded values for VSphere such as DC name, network name, etc.\n")
    print("Please ensure the values are correct from the iDLD doc!\n")
    print("To make things easier there are defaults to each value.\n")
    print("Please note that for DNS, if you have more that 1 DNS IP, you need to enclose the IP's in [] as per default.\n")

def main():

    today = time.strftime("%-d %B %Y")

    # Define the dict - with defaults
    dc = {
        "vcenter" : "10.0.29.39",
        "datacenter" : "DC-PROD",
        "cluster" : "prod-a-cluster",
        "datastore" : "DS-a-cluster",
        "network" : "vm-vlan102",
        "vmtemplate" : "RHEL85FT-Template",
        "vmname" : "terraformRHEL85FT-test",
        "hostname" : "terraformRHEL85FT-test",
        "dns_servers" : ["8.8.8.8", "1.1.1.1"],
        "domain" : "testlab.local",
        "gateway" : "192.168.102.254",
        "ipaddr" : "192.168.102",
        "mask" : "24",
        "lastoctet" : "105",
    }

    # Prompt user for input for each dict value or accept defaults and write to file
    print("\nPlease enter a valid value for each item:\n(Press ENTER to accept [defaults])\n")
    with open("terraform.tfvars", "w") as writef:
        writef.write(f"# terraform.tfvars\n# This file defines values for the variables declared in the variables.tf file.\n# Date: {today}\n\n")
        for keys, values in dc.items():
            dc[keys] = input(f"{keys} [{values}] : ") or values
            writef.write(f"{keys} = \"{dc[keys]}\"\n")

    # Display key value pairs for the dict for user to review
    print("\nYou have entered these values:\n")
    for keys, values in dc.items():
        print(f"{keys} = \"{values}\"")

    print("\n")


    # Further processing to correct the format for DNS list object - convert ' to " and remove "" from the DNS list []
    # The regex is contained in a TUPLE as the contents never change
    with open("terraform.tfvars", "r") as readf, open(".terratmp", "w") as writef:

        replacements = (
                        # ("(dns_servers = )(\")(\[.*\])(\")", "\\1\\3"),
                        ("\"(\[)|(\])\"", "\\1\\2"),
                        ("'", "\"")
        )

        content = readf.read()

        for pat, repl in replacements:
            content = re.sub(pat, repl, content, 0, re.MULTILINE)

        writef.write(content)


def output():
    # Copy .terratmp as terraform.tfvars
    shutil.copy(".terratmp", "terraform.tfvars")

    # Remove temp file .terratmp
    remove(".terratmp")

    # Print out further instructions for user
    print("\nThe file 'terraform.tfvars' has been created.\nPlease check and copy to the terraform project directory.\n")


def repeat():
    # Validate from user the data is correct
    answer = input("Is this correct? (Y/N): ")
    answer = answer.lower()

    if answer == "y":
        return False
    else:
        return True


''' Call the functions '''
welcome()
main()
while repeat():
    main()
output()
