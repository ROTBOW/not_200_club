import os
import smtplib
import ssl

import openpyxl
from alive_progress import alive_bar
from dotenv import load_dotenv

# loading the local .env file
load_dotenv()
# print(os.environ.get('anne-marie_russo'))

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
    
    
    def __format_name(self, name:str) -> str:
        return name.lower().replace(' ', '_')
    
    def __init__(self) -> None:
        self.__get_recent_file_path()
        self.no_emails = list()
        
        
    def scan_sheets(self) -> None:
        workbook = openpyxl.load_workbook(self.file_path)
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL('smtp.gmail.com', port=465, context=context) as server:
            server.login(os.getenv('email_user'), os.getenv('email_password'))
            for sheet in workbook.worksheets:
                if sheet.title in {'Overview', 'Issue Legend', 'Placements'}:
                    continue
                elif os.getenv(self.__format_name(sheet.title)) == None:
                    self.no_emails.append(sheet.title)
                    
                self.get_data_and_email(sheet, server)
            
                
    def get_data_and_email(self, sheet, server) -> None:
        sender_email = os.getenv('email_user')
        receiver_email = os.getenv(self.__format_name(sheet.title))
        
        # server.sendmail(sender_email, receiver_email, f'Hey {sheet.title}')
        
        
if __name__ == '__main__':
    em = Emailer()
    em.scan_sheets()