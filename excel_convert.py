# %%writefile tc.py
# v3
# copy/paste csv file into notepad++
# save as TC.csv in Linux
# Use cat TC.csv | column -t -s, > TC.txt

import time
import pandas as pd
import numpy as np


def excel_convert(excel_files):

    today = time.strftime("%Y%m%d")

    # Create new df and store selected columns
    excel_file = pd.read_excel(excel_files,
                               sheet_name='Invent',
                               usecols='B,C,I,J,L,N,Q,S,U,V',
                               index_col=False)

    #Strip white space from all columns
    excel_file.columns = excel_file.columns.str.strip()

    #Remove all leading or trailing spaces, or odd chars from cells
    excel_file = excel_file.replace( ['\s+$', '^\s+', ' - ', ' ', '_$', '^\s+_?', '^\s+$'],
                                     ['', '', '-'  , '_', ''  , '' , np.NaN],
                                     regex=True )

    #Enforce lowercase for columns.
    excel_file['HostName'] = excel_file['HostName'].str.lower()
    excel_file['iDRAC'] = excel_file['iDRAC'].str.lower()

    #Filter out rows we want.
    excel_file = excel_file[excel_file['OS'].str.contains('ESXi_7.0|vCenter_Server_6.7_U3j|RHEL_8.3|Windows_2019', na=False)]

    print(excel_file) # Debugging
    #Export results to excel sheet.
    return {excel_file.to_excel(f'new_{today}.xlsx', na_rep='NA', index=False),
            excel_file.to_csv(f'new_{today}.csv', na_rep='NA', index=False)
           }


def main():
    excel_convert('FT - Cloud Inventory IP V0.12.xlsx')

if __name__ == '__main__':
    main()
