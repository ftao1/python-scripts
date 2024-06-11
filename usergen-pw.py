#!/usr/bin/env python3

"""
Script        : usergen-pw.py
Description   : Python script to convert user list in passwd format to yml code
Dependencies  : ansible, python, ssh
Usage         : python3 usergen-pw.py /etc/passwd
Author        : Fai Tao
Version       : 0.3
Date          : 03 Oct 2020

Change history (most recent first)

Date          Who             Comments
----          ---             --------
03/10/20      FT              Added positional argument parsing and error checking
03/10/20      FT              Added interaction
02/10/20      FT              Initial draft
"""

import argparse
import sys

# Set up parser to look for command line arg and provide error handling
parser = argparse.ArgumentParser(description='Convert user list to yml.')
parser.add_argument('filename', help='The user list to read.')
parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')

args = parser.parse_args()

try:
    f = open(args.filename)

except FileNotFoundError as err:
    # print(f"Error: {err}")
    print(f"No such file: '{args.filename}'. Please provide user list. Exiting")
    sys.exit(2)

else:
    print("---\n", "# Ansible vars file for users\n","users:", sep="\n")
    with f:
        for lines in f:
            r = lines.rstrip()      # Strip the newline for each line
            r = r.split(':')        # Split on the : delimiter
            print(f"    - {{ username: '{r[0]}' , comment: '{r[4]}' , uid: '{r[2]}' , group: '{r[3]}' , shell: '{r[6]}' }}")

