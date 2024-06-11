#!/usr/bin/env python3

"""
Script        : usergen-csv.py
Description   : Python script to convert csv user list to yml vars file.
Dependencies  : ansible, python, ssh
Usage         : python3 usergen-csv.py userlist.csv
Author        : Fai Tao
Version       : 0.5
Date          : 12 May 2022

Change history (most recent first)

Date          Who             Comments
----          ---             --------
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

def main():
    '''
    Function to convert csv file to Ansible yml vars file for adding users
    '''
    # Set up parser to look for command line arg and provide error handling
    parser = argparse.ArgumentParser(description='Convert csv user list to yml vars file.')
    parser.add_argument('filename', help='The csv user list to read.')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.5')

    args = parser.parse_args()

    yml_header = "---\n\n# ANSIBLE VARS FILE FOR USERS\n# users:\n#  - { username: 'some user', comment: 'some comment', group: 'some group' }\n\nusers:\n"

    try:
        with open(args.filename, 'r') as infile, open('usersvar.yml.out', 'w+') as writefile:

            # headers = ['username', 'comment', 'gid']   # You can specify headers here and leave it out in the cvs file
            # csv_data = csv.DictReader(infile, headers) # But you must specify it here as an extra arg. Uncomment these 2 lines if the csv file does not have headers.

            csv_data = csv.DictReader(infile)            # Comment out this line if the csv files does not contain headers
            # writefile.write(f"---\n\n# ANSIBLE VARS FILE FOR USERS\n# users:\n#  - {{ username: 'some user', comment: 'some comment', group: 'some group' }}\n\nusers:\n")
            writefile.write(yml_header)

            for line in csv_data:
                if (not line['gid']) and (not line['comment']):
                    writefile.write(f"  - {{ username: '{line['username']}' }}\n")

                elif not line['comment']:
                    writefile.write(f"  - {{ username: '{line['username']}', group: '{line['gid']}' }}\n")

                elif not line['gid']:
                    writefile.write(f"  - {{ username: '{line['username']}', comment: '{line['comment']}' }}\n")

                else:
                    writefile.write(f"  - {{ username: '{line['username']}', comment: '{line['comment']}', group: '{line['gid']}' }}\n")


    except FileNotFoundError as err:
        print(f"No such file: '{args.filename}'. Please provide csv user list. Exiting")
        sys.exit(2)

    return writefile

if __name__=="__main__":
    main()

