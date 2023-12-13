import os

import openpyxl
from dotenv import load_dotenv

# loading the local .env file
# print(os.environ.get('josiah_leon'))
load_dotenv()

# Constants
DIR = os.path.dirname(os.path.realpath(__file__))
RES = os.path.join(DIR, 'res')


class Emailer:
    
    def __get_recent_file_path(self) -> None:
        """
        The function `__get_recent_file_path` finds the most recent file in res folder and sets the
        `file_path` attribute to the path of that file.
        """
        files = os.listdir(RES)
        most_recent_file = [0, '']
        for f in files:
            t = os.path.getmtime(os.path.join(RES, f))
            if t > most_recent_file[0]:
                most_recent_file = [t, f]
                
        self.file_path = os.path.join(RES, most_recent_file[1])
    
    def __init__(self) -> None:
        self.__get_recent_file_path()
        self.no_emails = list()
        
                
        
        
        
if __name__ == '__main__':
    em = Emailer()
    print(em.file_path)