import os
import re
from collections import defaultdict as ddict
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from statistics import mean, median, mode
from string import ascii_uppercase
from time import time

import requests
import xlsxwriter as xwriter
from alive_progress import alive_bar
from openpyxl import load_workbook

DIR = os.path.dirname(os.path.realpath(__file__))
TARGET = fr'{DIR}\\target'
RES = fr'{DIR}\\res'

class Not200Club:
    
    def __init__(self, workbook, timeout = None) -> None:
        """
        This is the initialization function for a class that takes a workbook and optional timeout
        parameter, and initializes various data structures and variables.
        
        :param workbook: This parameter is an object representing an Excel workbook. It is used to store
        and manipulate data in an Excel file
        :param timeout: The timeout parameter is an optional argument that can be passed to the
        constructor of an object. It specifies the maximum amount of time (in seconds) that the object
        should wait for a response before timing out. If no response is received within the specified
        timeout period, an exception is raised.
        """
        self.workbook = workbook
        self.data = list()
        self.sites_by_coach = ddict(lambda: ddict(dict))
        self.timeout = timeout
        self.total_seekers = 0
        
        overview_init = lambda: {'solo': 0, 'capstone': 0, 'group': 0}
        
        self.overview = {
            'sites_status': overview_init(),
            'sites_time': overview_init(),
            'sites_bad_url': overview_init(),
            'sites_no_url': overview_init(),
            'seeker_with_issue': 0,
            'time_average': list(),
            'sites_timeout': overview_init()
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
        self.total_seekers = sheet.max_row-1

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
                    if val == ' ' and idx == 1:
                        val = 'Placements' 
                    
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
    
    def __get_issues_from_urls(self, seeker: str, urls: dict) -> dict:
        """
        This function takes in a seeker and a dictionary of URLs, and returns a dictionary of issues for
        each URL, along with an overview of the number of issues encountered.
        
        :param seeker: The parameter "seeker" is a string that represents the name of the seeker or the
        person who is running the code
        :type seeker: str
        :param urls: The `urls` parameter is a dictionary containing project names as keys and their
        corresponding URLs as values
        :type urls: dict
        :return: a dictionary containing the issues found in the provided URLs. If no issues are found,
        an empty dictionary is returned. The dictionary is nested within another dictionary with the key
        'seeker'.
        """
        site_issues = ddict(dict)
        
        for proj, url in urls.items():
            if url != '':
                try:
                    res = requests.get(url, timeout=self.timeout)
                    if res.elapsed > timedelta(seconds=10):
                        site_issues[proj]['time'] = res.elapsed
                        self.overview['sites_time'][proj] += 1
                        self.overview['time_average'].append(res.elapsed.seconds)
                                
                    if res.status_code != 200:
                        site_issues[proj]['status'] = res.status_code
                        self.overview['sites_status'][proj] += 1
                        
                except requests.exceptions.Timeout:
                    site_issues[proj]['timeout'] = f'URL timeout at {self.timeout}s'
                    self.overview['sites_timeout'][proj] += 1
                    
                except Exception as e:
                    site_issues[proj]['bad_url'] = str(e)
                    self.overview['sites_bad_url'][proj] += 1
            else:
                site_issues[proj]['no-link'] = True
                self.overview['sites_no_url'][proj] += 1
            
        return {seeker: site_issues} if site_issues else {}
    
    def __threading_get_all_issues(self, coach: str) -> dict:
        """
        This function uses multithreading to gather all issues from URLs associated with a given coach.
        
        :param coach: The coach parameter is a string representing the name of the coach for whom we
        want to get all the issues
        :type coach: str
        :return: a dictionary containing all the issues gathered from the URLs of the seekers assigned
        to the given coach.
        """
        seekers = self.sites_by_coach[coach]
        all_issues = dict()
        
        with ThreadPoolExecutor(max_workers=20) as pool:
            futures = list()
            for seeker in seekers:
                urls = {
                        'solo': self.__validate_url(seekers[seeker]['solo']),
                        'capstone': self.__validate_url(seekers[seeker]['capstone']),
                        'group': self.__validate_url(seekers[seeker]['group'])
                    }
                futures.append(pool.submit(self.__get_issues_from_urls, seeker, urls))
            
            with alive_bar(len(futures), title=f"Gathering threads for {coach}") as bar:
                for f in futures:
                    all_issues.update(f.result())
                    bar()
        
        return all_issues
    
    def __test_urls_and_write_to_xlsx(self) -> None:
        """
        This function iterates through a dictionary of websites by coach, validates the URLs, gets
        issues from the URLs, and writes the issues to an Excel sheet.
        """
        
        for coach in self.sites_by_coach:
            col = 1
            sheet = self.workbook._add_sheet(coach)
            all_coach_issues = self.__threading_get_all_issues(coach)
            
            
            if all_coach_issues:
                for seeker, issues in all_coach_issues.items():
                    status = self.sites_by_coach[coach][seeker]['status']
                    self.overview['seeker_with_issue'] += 1
                    row = 2
                    sheet.write(f'A{col}', seeker)
                    sheet.write(f'B{col}', status)
                    for proj in ['solo', 'capstone', 'group']:
                        if issues[proj]:
                            sheet.write(f'{self.__idx_to_letter(row)}{col}', proj)
                            row += 1
                            for issue, v in issues[proj].items():
                                sheet.write(f'{self.__idx_to_letter(row)}{col}', f'{issue}: {v}')
                                row += 1
                    col += 1
                    
                
    def __fill_overview(self) -> None:
        """
        This function fills in an Excel sheet with various statistics related to website loading issues.
        """
        sheet = self.workbook._add_sheet('Overview')
        
        sheet.write('A1', 'TOTAL SEEKERS WITH ISSUES')
        sheet.write('B1', f"{self.overview['seeker_with_issue']}/{self.total_seekers}")
        
        sheet.write('A2', 'SITES WITH TIMES 10s>')
        sheet.write('B2', f'Total: {sum(self.overview["sites_time"].values())}')
        sheet.write('C2', f'Solo: {self.overview["sites_time"]["solo"]}')
        sheet.write('D2', f'Capstone: {self.overview["sites_time"]["capstone"]}')
        sheet.write('E2', f'Group: {self.overview["sites_time"]["group"]}')
        
        sheet.write('A3', 'LOADING TIME STATS')
        if self.overview['time_average']:
            sheet.write('B3', f'Mean: {round(mean(self.overview["time_average"]), 2)}s')
            sheet.write('C3', f'Mode: {round(mode(self.overview["time_average"]), 2)}s')
            sheet.write('D3', f'Median: {round(median(self.overview["time_average"]), 2)}s')
        else:
            sheet.write('B3', 'No loading issues found')
            
        
        if self.timeout:
            sheet.write('A4', 'SITES THAT TIMEOUT')
            sheet.write('B4', f"Total: {sum(self.overview['sites_timeout'].values())}")
            sheet.write('C4', f"Solo: {self.overview['sites_timeout']['solo']}")
            sheet.write('D4', f"Capstone: {self.overview['sites_timeout']['capstone']}")
            sheet.write('E4', f"Group: {self.overview['sites_timeout']['group']}")
        else:
            sheet.write('A4', 'TIMEOUT NOT SET')
            
        
        sheet.write('A5', 'SITES WITH NO URLS')
        sheet.write('B5', f"Total: {sum(self.overview['sites_no_url'].values())}")
        sheet.write('C5', f"Solo: {self.overview['sites_no_url']['solo']}")
        sheet.write('D5', f"Capstone: {self.overview['sites_no_url']['capstone']}")
        sheet.write('E5', f"Group: {self.overview['sites_no_url']['group']}")
        
        sheet.write('A6', 'SITES WITH BAD URLS')
        sheet.write('B6', f"Total: {sum(self.overview['sites_bad_url'].values())}")
        sheet.write('C6', f"Solo: {self.overview['sites_bad_url']['solo']}")
        sheet.write('D6', f"Capstone: {self.overview['sites_bad_url']['capstone']}")
        sheet.write('E6', f"Group: {self.overview['sites_bad_url']['group']}")
        
        sheet.write('A7', 'SITES WITH BAD STATUS')
        sheet.write('B7', f"Total: {sum(self.overview['sites_status'].values())}")
        sheet.write('C7', f"Solo: {self.overview['sites_status']['solo']}")
        sheet.write('D7', f"Capstone: {self.overview['sites_status']['capstone']}")
        sheet.write('E7', f"Group: {self.overview['sites_status']['group']}")
        
        
        
    
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
    start = time()
    n2c = Not200Club(workbook, timeout = 120)
    n2c.main()
    workbook.close()
    end = time()
    print(f'\nTotal Time to complete: {round(end-start, 2)}s')