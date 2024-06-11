#!/usr/bin/env python3


'''
Script        : usergen5.py
Description   : Converts text list of users to yml
Dependencies  : python
Usage         : ./usergen5.py userfile.txt
Author        : Fai Tao
Version       : 0.2
Date          : 06 Oct 2020

Change history (most recent first)

Date            Who         Comments
----            ---         --------
27/10/20        FT          Check data is clean
08/10/20        FT          Converted to functions
02/10/20        FT          Initial draft
'''

import argparse
import sys


def get_args():
    parser = argparse.ArgumentParser(description='Convert user list to yml.')
    parser.add_argument('filename', help='The user list to read.')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    return parser.parse_args()


def main():
    args = get_args()
    try:
        file = open(args.filename)

    except FileNotFoundError as err:
        print(f"{err}. No such file: '{args.filename}'. Please provide text user list, eg user.txt. Exiting")
        sys.exit(2)

    else:
        print("---\n", "# Ansible vars file for users\n", "users:", sep="\n")
        with file:
            for lines in file:
                ''' Ignore/skip blank or incomplete lines that do not contain 7 fields with continue '''
                # if len(lines.split(':')) < 7 or len(lines.split(':')) > 7:
                # if not len(lines.split(':')) == 7:
                if len(lines.split(':')) != 7:
                    continue
                row = lines.strip()
                row = row.split(':')
                print(f"    - {{ username: '{row[0]}' , comment: '{row[4]}' , uid: '{row[2]}' , group: '{row[3]}' , shell: '{row[6]}' }}")


if __name__ == '__main__':
    main()
