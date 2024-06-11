#!/usr/bin/env python3

"""
Script        : usergen-csv.py
Description   : Python script to convert csv user list to yml vars file.
Dependencies  : ansible, python, ssh
Usage         : python3 usergen-csv.py userlist.csv
Author        : Fai Tao
Version       : 0.8
Date          : 31 May 2022

Change history (most recent first)

Date          Who             Comments
----          ---             --------
31/05/22      FT              Improved error checking to ensure csv are free from extra spaces etc.
24/05/22      FT              Added extra comments for optional csv headers and strip() for each field
23/05/22      FT              Moved main() to convert_to_yml()
12/05/22      FT              Improved yml_header format to use single string
12/05/22      FT              Added optional headers list
11/05/22      FT              Changed to func
11/05/22      FT              Improved error checking and simplified input file to csv format
03/10/20      FT              Added positional argument parsing and error checking
03/10/20      FT              Added interaction
02/10/20      FT              Initial draft
"""

import csv
import argparse
import sys
import re

def main():
    convert_to_yml()

def row_clean_pass1(row1):
    ''' Remove whitespace at the start/end of each string in list'''
    return [item.strip() for item in row1]


def row_clean_pass2(row2):
    ''' Ensure there is one space between words'''
    return [ re.sub(r"\s+", " ", item) for item in row2 ]



def convert_to_yml():
    '''
    Function to convert csv file to Ansible yml vars file for adding users
    '''
    # Set up parser to look for command line arg and provide error handling
    parser = argparse.ArgumentParser(description='Convert csv user list to yml vars file.')
    parser.add_argument('filename', help='The csv user list to read.')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.8')

    args = parser.parse_args()

    yml_header = "---\n\n# ANSIBLE VARS FILE FOR USERS\n# users:\n#  - { username: 'some user', comment: 'some comment', group: 'some group' }\n\nusers:\n"

    try:
        with open(args.filename, 'r') as infile, open('usersvar.yml.out', 'w+', newline='' ) as writefile:

            # headers = ['username', 'comment', 'gid']   # You can specify headers here and leave it out in the csv file
            # csv_data = csv.DictReader(infile, headers) # But you must specify it here as an extra arg. Uncomment these 2 lines if the csv file does not have headers.

            csv_data = csv.reader(infile)            # Comment out this line if the csv files does not contain headers
            writefile.write(yml_header)

            next(csv_data, None)                         # skip the headers



            for row in csv_data:
                # Lets clean the csv file before doing anything else:
                cleaned_row = row_clean_pass1(row_clean_pass2(row))

                if len(cleaned_row) > 3:
                    continue

                if not cleaned_row[0]:
                    continue

                if len(cleaned_row) == 1:
                    writefile.write(f"  - {{ username: '{cleaned_row[0]}' }}\n")

                elif not cleaned_row[1]:
                    writefile.write(f"  - {{ username: '{cleaned_row[0]}', group: '{cleaned_row[2]}' }}\n")

                elif not cleaned_row[2]:
                    writefile.write(f"  - {{ username: '{cleaned_row[0]}', comment: '{cleaned_row[1]}' }}\n")

                else:
                    writefile.write(f"  - {{ username: '{cleaned_row[0]}', comment: '{cleaned_row[1]}', group: '{cleaned_row[2]}' }}\n")


    except FileNotFoundError as err:
        print(f"No such file: '{args.filename}'. Please provide csv user list. Exiting")
        sys.exit(2)

    return writefile

if __name__=="__main__":
    main()
