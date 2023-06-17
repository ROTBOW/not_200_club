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
    
    def __validate_url(self, url: str) -> str:
        """
        This function validates a URL by adding 'https://' to the beginning if it is not already
        present.
        
        :param url: The parameter `url` is a string that represents a URL
        :type url: str
        :return: a string that is either the input `url` if it starts with 'https://', or a modified
        version of the input `url` with 'https://' added to the beginning if it does not start with
        'https://'. If the input `url` is an empty string, the function returns an empty string.
        """
        
        if not url:
            return ''
        
        if not url.startswith('https://'):
            return 'https://' + url
        
        return url
    
    def __get_issues_from_url(self, url: str) -> dict:
        """
        This function takes a URL as input and returns a dictionary containing any issues found with the
        URL, such as a slow response time or a non-200 status code.
        
        :param url: A string representing the URL of a website to be checked for issues
        :type url: str
        :return: A dictionary containing information about any issues encountered while trying to access
        the provided URL. The dictionary may contain keys such as 'time', 'status', 'bad_url', or
        'no-link', depending on the specific issue encountered.
        """
        site_issues = dict()
        
        if url != '':
            try:
                res = requests.get(url)
                if res.elapsed > timedelta(seconds=10):
                    site_issues['time'] = res.elapsed
                            
                if res.status_code != 200:
                    site_issues['status'] = res.status_code
            except Exception as e:
                print('***** BAD URL *****', url, e)
                site_issues['bad_url'] = str(e)
        else:
            site_issues['no-link'] = True
            
        return site_issues
    
    
    def __test_urls_and_write_to_xlsx(self) -> None:
        """
        This function iterates through a dictionary of websites by coach, validates the URLs, gets
        issues from the URLs, and writes the issues to an Excel sheet.
        """
        for coach in self.sites_by_coach:
            col = 1
            sheet = self.workbook._add_sheet(coach.replace(' ', '_'))
            
            with alive_bar(len(self.sites_by_coach[coach]), title=f'Checking {coach}\'s Seekers') as bar:
                for seeker in self.sites_by_coach[coach]:
                    url = self.__validate_url(self.sites_by_coach[coach][seeker])
                    site_issues = self.__get_issues_from_url(url)
                        
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