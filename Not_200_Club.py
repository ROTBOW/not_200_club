import os
import re
from collections import defaultdict as ddict
from datetime import date, timedelta
from string import ascii_uppercase

import requests
import xlsxwriter as xwriter
from alive_progress import alive_bar
from openpyxl import load_workbook

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
        self.sites_by_coach = ddict(lambda: ddict(dict))
        
        self.overview = {
            'sites_status': 0,
            'sites_time': 0,
            'sites_bad_url': 0,
            'sites_no_url': 0,
            'seeker_with_issue': 0
        }
        
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
        This function reads data from an Excel file in the target folder and populates a dictionary with the data.
        """
        target_file = os.listdir(TARGET)[0]
        data = load_workbook(fr'{TARGET}\\{target_file}')
        sheet = data.active

        with alive_bar(sheet.max_row-1, title="Grabing Data...") as bar:
            for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
                curr_row = dict()
                for idx, cell in enumerate(row):
                    
                    data_list = {
                        0: 'seeker',
                        1: 'coach',
                        2: 'status',
                        3: 'solo',
                        4: 'capstone',
                        5: 'group'
                    }
                    
                    val = cell.value
                    if not val and idx == 1:
                        val = cell.value if cell.value != ' ' else 'Placements'
                    
                    curr_row[data_list[idx]] = val
                    
                        
                
                for proj in ['status', 'solo', 'capstone', 'group']:
                    self.sites_by_coach[curr_row['coach']][curr_row['seeker']][proj] = curr_row[proj]
                bar()
    
    def __validate_url(self, url: str) -> str:
        """
        This function validates a given URL and adds "https://" if it is missing.
        
        :param url: The `url` parameter is a string that represents a URL
        :type url: str
        :return: a string that represents a validated URL. If the input URL is empty, it returns an
        empty string. If the input URL does not start with "http://" or "https://", it adds "https://"
        to the beginning of the URL and returns it. Otherwise, it returns the input URL as is.
        """
        if not url:
            return ''
        
        if not re.match(r'^http[s]?:\/\/', url):
            return 'https://' + url
        
        return url
    
    def __get_issues_from_urls(self, urls: dict) -> dict:
        """
        This function takes in a dictionary of URLs and returns a dictionary of issues for each URL,
        including response time, status code, and bad URLs.
        
        :param urls: A dictionary where the keys are project names and the values are URLs associated
        with those projects
        :type urls: dict
        :return: a dictionary containing information about issues with URLs. The keys of the dictionary
        are project names, and the values are dictionaries containing information about issues with the
        corresponding URL. The information includes the time it took to get a response from the URL, the
        status code of the response, and any errors that occurred while trying to access the URL. The
        function also updates a separate dictionary called "overview
        """
        site_issues = ddict(dict)
        
        for proj, url in urls.items():
            if url != '':
                try:
                    res = requests.get(url)
                    if res.elapsed > timedelta(seconds=10):
                        site_issues[proj]['time'] = res.elapsed
                        self.overview['sites_time'] += 1
                                
                    if res.status_code != 200:
                        site_issues[proj]['status'] = res.status_code
                        self.overview['sites_status'] += 1
                except Exception as e:
                    site_issues[proj]['bad_url'] = str(e)
                    self.overview['sites_bad_url'] += 1
            else:
                site_issues[proj]['no-link'] = True
                self.overview['sites_no_url'] += 1
            
        return site_issues
    
    
    def __has_issues(self, issues: dict):
        """
        The function checks if there are any issues in the given dictionary for solo, capstone, and
        group projects.
        
        :param issues: The parameter 'issues' is a dictionary that contains three keys: 'solo',
        'capstone', and 'group'. The values associated with each key are lists of issues. The function
        checks if any of these lists have a length greater than zero and returns a boolean value
        accordingly
        :type issues: dict
        :return: a boolean value indicating whether there are any issues in the input dictionary. It
        checks if the length of the 'solo', 'capstone', and 'group' lists in the 'issues' dictionary are
        greater than zero, and returns True if at least one of them is non-empty, and False otherwise.
        """
        return any([len(issues['solo']), len(issues['capstone']), len(issues['group'])])
    
    def __test_urls_and_write_to_xlsx(self) -> None:
        """
        This function iterates through a dictionary of websites by coach, validates the URLs, gets
        issues from the URLs, and writes the issues to an Excel sheet.
        """
        for coach in self.sites_by_coach:
            col = 1
            sheet = self.workbook._add_sheet(coach)
            
            with alive_bar(len(self.sites_by_coach[coach]), title=f'Checking {coach}\'s Seekers') as bar:
                for seeker in self.sites_by_coach[coach]:
                    status = self.sites_by_coach[coach][seeker]['status']
                    urls = {
                        'solo': self.__validate_url(self.sites_by_coach[coach][seeker]['solo']),
                        'capstone': self.__validate_url(self.sites_by_coach[coach][seeker]['capstone']),
                        'group': self.__validate_url(self.sites_by_coach[coach][seeker]['group'])
                    }
                    site_issues = self.__get_issues_from_urls(urls)
                        
                    if self.__has_issues(site_issues):
                        self.overview['seeker_with_issue'] += 1
                        row = 2
                        sheet.write(f'A{col}', seeker)
                        sheet.write(f'B{col}', status)
                        for proj in ['solo', 'capstone', 'group']:
                            if site_issues[proj]:
                                sheet.write(f'{self.__idx_to_letter(row)}{col}', proj)
                                row += 1
                                for issue, v in site_issues.items():
                                    sheet.write(f'{self.__idx_to_letter(row)}{col}', f'{issue}: {v}')
                                    row += 1
                        col += 1
                    bar()
                
    def __fill_overview(self) -> None:
        """
        This function fills in an Excel sheet with data related to various issues found during a website
        check.
        """
        sheet = self.workbook._add_sheet('Overview')
        
        sheet.write('A1', 'TOTAL SEEKERS WITH ISSUES')
        sheet.write('B1', self.overview['seeker_with_issue'])
        
        sheet.write('A2', 'TOTAL SITES WITH TIMES 10s>')
        sheet.write('B2', self.overview['sites_time'])
        
        sheet.write('A3', 'TOTAL SITES WITH NO URLS')
        sheet.write('B3', self.overview['sites_no_url'])
        
        sheet.write('A4', 'TOTAL SITES WITH BAD URLS')
        sheet.write('B4', self.overview['sites_bad_url'])
        
        sheet.write('A5', 'TOTAL SITES WITH BAD STATUS')
        sheet.write('B5', self.overview['sites_status'])
        
        
    
    def main(self) -> None:
        """
        The main function grabs data from a file and tests URLs before writing the results to an Excel
        file.
        """
        self.__grab_data_from_file()
        self.__test_urls_and_write_to_xlsx()
        self.__fill_overview()
        
        
 

if __name__ == '__main__':
    if not os.path.isdir(RES):
        os.mkdir(RES)
    
    workbook = xwriter.Workbook(f'res\{date.today()}.xlsx')
    n2c = Not200Club(workbook)
    n2c.main()
    workbook.close()