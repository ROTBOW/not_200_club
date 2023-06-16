import os
from collections import defaultdict as ddict
from datetime import date, timedelta
import requests

import xlsxwriter as xwriter
from alive_progress import alive_bar
from openpyxl import load_workbook
from string import ascii_uppercase

DIR = os.path.dirname(os.path.realpath(__file__))
TARGET = fr'{DIR}\\target'
RES = fr'{DIR}\\res'
    
class Not200Club:
    
    def __init__(self, workbook) -> None:
        """
        This is a constructor function that initializes variables including a workbook, a list, and a
        dictionary.
        
        :param workbook: The "workbook" parameter is likely a reference to an Excel workbook object that
        will be used to read or write data to an Excel file. The code is initializing an instance of a
        class and setting the "workbook" attribute to the passed in workbook object
        """
        self.workbook = workbook
        self.data = list()
        self.sites_by_coach = ddict(dict)
        
    def __idx_to_letter(self, idx: int) -> str:
        """
        This function converts an index number to a corresponding letter in the alphabet using ASCII
        uppercase characters.
        
        :param idx: idx is an integer representing the index of a letter in the alphabet. The function
        is designed to convert this index to its corresponding letter
        :type idx: int
        :return: a string that represents the corresponding letter(s) for the given index. The letters
        are determined based on the position of the index in the alphabet, with A being 0, B being 1,
        and so on. The function uses the ascii_uppercase string to map the remainder of the index
        divided by 26 to the corresponding letter, and then continues to divide the index by
        """
        result = ""
        while idx >= 0:
            remainder = idx % 26  # Get the remainder of idx divided by 26
            result = ascii_uppercase[remainder] + result
            idx = (idx // 26) - 1

        return result
        
        
    def __grab_data_from_file(self) -> None:
        """
        This function reads data from an Excel file and populates a dictionary with the data.
        """
        target_file = os.listdir(TARGET)[0]
        data = load_workbook(fr'{TARGET}\\{target_file}')
        sheet = data.active

        with alive_bar(sheet.max_row-1, title="grabing data...") as bar:
            for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
                curr_row = dict()
                for idx, cell in enumerate(row):
                    if idx == 0:
                        curr_row['seeker'] = cell.value
                    elif idx == 1:
                        curr_row['coach'] = cell.value if cell.value != ' ' else 'Placements'
                    else:
                        curr_row['url'] = cell.value
                    
                
                self.sites_by_coach[curr_row['coach']][curr_row['seeker']] = curr_row['url']
                bar()
    
    
    def __test_urls_and_write_to_xlsx(self) -> None:
        """
        This function checks URLs for a list of seekers and writes any issues found to an Excel file,
        organized by coach.
        """
        for coach in self.sites_by_coach:
            col = 1
            sheet = self.workbook._add_sheet(coach.replace(' ', '_'))
            
            with alive_bar(len(self.sites_by_coach[coach]), title=f'Checking {coach}\'s Seekers') as bar:
                for seeker in self.sites_by_coach[coach]:
                    
                    site_issues = dict()
                    if self.sites_by_coach[coach][seeker] != '':
                        try:
                            res = requests.get(self.sites_by_coach[coach][seeker])
                            if res.elapsed > timedelta(seconds=10):
                                site_issues['time'] = res.elapsed
                            
                            if res.status_code != 200:
                                site_issues['status'] = res.status_code
                        except Exception as e:
                            print('***** BAD URL *****', seeker, e)
                            site_issues['bad_url'] = str(e)
                    else:
                        site_issues['no-link'] = True
                        
                        
                    if len(site_issues) != 0:
                        sheet.write(f'A{col}', seeker)
                        for idx, (issue, v) in enumerate(site_issues.items()):
                            sheet.write(f'{self.__idx_to_letter(idx+1)}{col}', f'{issue}: {v}')
                        col += 1
                    bar()
                
        
    
    def main(self) -> None:
        """
        The main function grabs data from a file and tests URLs before writing the results to an Excel
        file.
        """
        self.__grab_data_from_file()
        self.__test_urls_and_write_to_xlsx()
        
        
 

if __name__ == '__main__':
    if not os.path.isdir(RES):
        os.mkdir(RES)
    
    workbook = xwriter.Workbook(f'res\{date.today()}.xlsx')
    n2c = Not200Club(workbook)
    n2c.main()
    workbook.close()