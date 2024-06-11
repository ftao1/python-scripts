# Convert csv files into Excel workbook
# Format col widths to fixed width
#

import time, socket
import pandas as pd
from pandas.io.excel import ExcelWriter
from pathlib import Path
from openpyxl import load_workbook
from string import ascii_uppercase

today = time.strftime("%Y%m%d")
csv_path = Path('.')

def get_host():
    '''Get the hostname'''
    fqdn = socket.gethostname()
    '''Create dict with hostnames to friendly names'''
    env = {
        "devA-001.example.com" : "devA",
        "prodA-001.example.com" : "prodA",
        "prodB-001.example.com" : "prodB",
        "WorkLaptop" : "laptop",
        "ThinkPad" : "thinkpad",
        }
    return env.get(fqdn)


def  create_report(dir1):
    '''Look for csv files in dir and create a list of filenames'''
    csv_files_list = [file.stem for file in csv_path.glob('*.csv')]

    '''Create new workbook and add each csv in own sheet'''
    with ExcelWriter('temp.xlsx') as ew:
         for csv_file in csv_files_list:
            pd.read_csv(csv_file + '.csv').to_excel(ew, sheet_name=csv_file, index=False)


def format_width(wbook):
    '''Load workbook created from create_report func'''
    wb = load_workbook(wbook)

    '''Interate over total nmuber of sheets and adjust column widths
       Work out the total number of worksheets, and set each one active'''
    for i in range(len(wb.worksheets)):
        wb.active = i
        '''For each worksheet set the col width for A,B,C, leave the others at default'''
        for column in ascii_uppercase:
            if (column=='A' or column=='B' or column=='C'):
                wb.active.column_dimensions[column].width = 50
            else:
                wb.active.column_dimensions[column].width = 8
    '''Save final workbook'''
    wb.save(f'{get_host()}_rpm_excel_{today}.xlsx')


'''Call the functions'''
create_report(csv_path)
time.sleep(1)
format_width('temp.xlsx')

