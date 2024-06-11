"""
Script        : usergen-csv-pd.py
Description   : Python script to convert csv user list to yml vars file using pandas.
Dependencies  : ansible, python, ssh
Usage         : python3 usergen-csv-2.py userlist.csv
Author        : Fai Tao
Version       : 0.2
Date          : 22 June 2022

Change history (most recent first)

Date        Who     Comments
----        ---     --------
22/06/22    FT      Added cleaning func to remove invalid username and gid
17/06/22    FT      Initial draft based on previous usergen-csv-2.py
"""

import pandas as pd
import numpy as np
from os import system
from easygui import fileopenbox, textbox

def welcome():
    """
    Display welcome message at the prompt.
    """

    system('cls')
    mesg = ["Welcome.\n\nThis script will help you create the 'usersvar.yml' file for Ansible users role.",
            "The usersvar.yml file contains the users you wish to add to remote systems using Ansible.",
            "The script will prompt you to select the Excel file as input and outputs to the 'usersvar.yml.out.txt' file.\n",
            "The Excel file should be in the agreed format in columns A, B, C:\n",
            "Username, Comment, GID\n",
            "Username is mandatory. Comment and GID are optional.",
            "However it is considered best practice to include a comment for all users to identify them.\n",
            "Invalid username and gid will be excluded. Please check your source data.\n\n",
            "Follow the instructions in the popup message box at the end.",
           ]
    print('\n'.join(mesg))


def openfile():
    """
    Open the Excel file as input. It is assumed that the input file is valid with correct values
    """

    excel_file = fileopenbox("Excel File Selection", "Choose a Microsoft Excel (*.xlsx) file:", default="*.xlsx")
    if excel_file is None:
        print("\nYou have quit the program.\n")
        sys.exit(0)

    # Return the name of the excel file as a csv text file for further processing
    return excel_file


def message():
    """
    Display message upon completetion of process.
    """

    message = "Process completed!"
    title = "Process completed!"
    text = ["Your file has been saved as 'usersvar.yml.out.txt' in the same local folder.\n\n",
            "You can now use this file as the user list in the vars folder for the Ansible users role.\n\n",
            "Simply open the 'usersvar.yml.out.txt' and copy/paste into the usersvar.yml on the Ansible server.\n\n\n",
            "Click OK/Cancel to dismiss.\n"
            ]

    return textbox(message, title, text)


def cleaned():
    """
    Function to clean the data. Remove extraneous spaces, invalid usernames, gid
    """

    # Create new df and store selected columns
    excel_file = pd.read_excel(openfile(),
                               usecols='A,B,C',
                               index_col=False,
                               dtype='str')


    # Remove all leading or trailing spaces, or odd chars from cells
    excel_file = excel_file.replace( ['^\s+$', '\s+$', '^\s+', '\s+'],
                                     [np.NaN, '', '', ' '],
                                     regex=True )

    # Remove rows containing invalid usernames or gid containing spaces
    for crud in ['gid', 'username']:
        excel_file[f'crud_{crud}'] = excel_file[crud].str.count(r'\s') + 1    # create test cols and count words to identify invalid fields in rows
        excel_file.drop(excel_file.index[excel_file[f'crud_{crud}'] >= 2.0], inplace = True) # drop those rows
        excel_file.drop(columns=f'crud_{crud}', axis=1, inplace = True) # remove test cols

    return excel_file


def yml_convert():
    """
    Function to convert csv file to Ansible yml vars file for adding users
    """
    with open('usersvar.yml.out.txt', 'w+', newline='') as writefile:

        yml_header = ["---\n\n# ANSIBLE VARS FILE FOR USERS",
                      "# users:",
                      "#  - { username: 'some_user', comment: 'some comment', group: 'some_group' }\n",
                      "users:\n",
                     ]
        # Write out the yml header
        writefile.write('\n'.join(yml_header))


        for index, row in cleaned().iterrows():
            if pd.isna(row['username']):
                continue

            if (pd.isna(row['gid'])) and (pd.isna(row['comment'])):
                writefile.write(f"  - {{ username: '{row['username']}' }}\n")

            elif pd.isna(row['comment']):
                writefile.write(f"  - {{ username: '{row['username']}', group: '{row['gid']}'}}\n")

            elif pd.isna(row['gid']):
                writefile.write(f"  - {{ username: '{row['username']}', comment: '{row['comment']}'}}\n")

            else:
                writefile.write(f"  - {{ username: '{row['username']}', comment: '{row['comment']}', group: '{row['gid']}'}}\n")

    return writefile

def main():
    welcome()
    yml_convert()
    message()

if __name__ == '__main__':
    main()
