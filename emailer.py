import os
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import openpyxl
from alive_progress import alive_bar
from dotenv import load_dotenv

# loading the local .env file
load_dotenv()

# Constants
DIR = os.path.dirname(os.path.realpath(__file__))
RES = os.path.join(DIR, 'res')


class Emailer:
    
    def __get_recent_file_path(self) -> None:
        """
        The function finds the most recent file in res folder and sets the
        `file_path` attribute to the path of that file.
        """
        files = os.listdir(RES)
        most_recent_file = [0, '']
        for f in files:
            t = os.path.getmtime(os.path.join(RES, f))
            if t > most_recent_file[0]:
                most_recent_file = [t, f]
                
        self.file_path = os.path.join(RES, most_recent_file[1])
        self.__validate_file()
        
    
    
    def __format_name(self, name:str) -> str:
        """
        The function takes a name, converts it to lowercase, and replaces spaces with
        underscores.
        
        :param name: The parameter `name` is a string that represents a person's name
        :type name: str
        :return: the name in lowercase with spaces replaced by underscores.
        """
        return name.lower().replace(' ', '_')
    
    
    def __validate_file(self) -> None:
        """
        The function validates if the file's creation date matches today's date and prompts the user for
        confirmation before proceeding with the emailer.
        """
        d = datetime.fromtimestamp(os.path.getctime(self.file_path))
        today = datetime.now()
        if not all([today.day == d.day, today.month == d.month, today.year == d.year]):
            print('File\'s date does not match today\'s date!')
            print(f'    - today: {today.month}-{today.day}-{today.year}')
            print(f'    -  file: {d.month}-{d.day}-{d.year}')
            print('Are you sure you want to go ahead with the emailer?')
            ans = input('-> ')
            if ans not in ['yes', 'y']:
                raise ValueError('Date Mismatch')
            
    
    
    def __init__(self) -> None:
        self.__get_recent_file_path()
        self.no_emails = list()
        
        
    def scan_sheets(self) -> None:
        """
        The `scan_sheets` function scans through sheets in an Excel workbook, skips certain sheets, and
        sends data from other sheets via email.
        """
        workbook = openpyxl.load_workbook(self.file_path)
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL('smtp.gmail.com', port=465, context=context) as server:
            server.login(os.getenv('email_user'), os.getenv('email_password'))
            
            title = 'Getting Coach\'s summery and emailing...'
            with alive_bar(len(workbook.worksheets), title=title) as bar:
                for sheet in workbook.worksheets:
                    if sheet.title in {'Overview', 'Issue Legend', 'Placements'}:
                        continue
                    elif os.getenv(self.__format_name(sheet.title)) == None:
                        self.no_emails.append(sheet.title)
                        continue
                    
                    bar.title(f'Getting {sheet.title.split(" ")[0]}\'s summery and emailing...')
                    self.get_data_and_email(sheet, server)
                    
                    bar()
                
        if self.no_emails:
            print('the following names didn\'t have a email listed')
            print(self.no_emails)
                
            
                
    def get_data_and_email(self, sheet, server) -> None:
        """
        This function retrieves data from a sheet, analyzes it, and sends an email with a summary of the
        analysis.
        
        :param sheet: The `sheet` parameter is the spreadsheet object that contains the data. It is used
        to iterate over the rows and retrieve the necessary information for the email
        :param server: The `server` parameter is the SMTP server object that is used to send the email.
        It should be an instance of the `smtplib.SMTP` class
        """
        sender_email = os.getenv('email_user')
        receiver_email = os.getenv(self.__format_name(sheet.title))
        
        danger_zone = list()
        time = 0
        redzone = 0
        
        for row in sheet.iter_rows():
            name, status, solo, capstone, group = (x.value for x in row)
            if status == 'Seeker Status':
                continue
            
            if 'No Issues Found' not in (solo, capstone, group):
                danger_zone.append([name, status])
                
            for proj in (solo, capstone, group):
                if proj.startswith('time:'):
                    time += 1
                if proj.split(':')[0] in ('timeout', 'status', 'bad_url', 'no-link'):
                    redzone += 1
            
        message = MIMEMultipart("alternative")
        message["Subject"] = "Seeker Site Health Summary"
        message["From"] = sender_email
        message["To"] = receiver_email
        text = f'''\
            Hey {sheet.title.split(' ')[0]},
            
            Here is a summary of the site health check of your seekers!
            If you would like a more detailed view you can find the most recent health checks here:
            https://drive.google.com/drive/u/1/folders/1IlVrDq3EJBUKzVdbLhpIjuzWyNcJ-m-I
            
            Danger Zone Seekers: {len(danger_zone)}
            {', '.join([f"{seeker[0]} ({seeker[1]})" for seeker in danger_zone])}
            
            Time Issues: {time}
            
            Red Zone Issues: {redzone}
            
            
            This is an automated email please do not reply directly, if you are running into issues (or would like to not get these)
            reach out to Josiah Leon, jleon@appacademy.io'''
        html = f'''\
        <html>
            <body>
                <p>Hey {sheet.title.split(' ')[0]},<br/><br/>
                Here is a summary of the site health check of your seekers!<br/>
                If you would like a more detailed view you can find the most recent health checks <a href="https://drive.google.com/drive/u/1/folders/1IlVrDq3EJBUKzVdbLhpIjuzWyNcJ-m-I">here</a><br/><br/>
                
                Danger Zone Seekers: {len(danger_zone)} - (Meaning all projects are down or not working!)<br/>
                <ol>
                    {''.join([f"<li>{seeker[0]} ({seeker[1]})</li><br/>" for seeker in danger_zone])}
                </ol><br/>
                
                Time Issues: {time}<br/><br/>
                
                Red Zone Issues: {redzone}<br/><br/><br/>
                
                <i>This is an automated email please do not reply directly, if you are running into issues (or would like to not get these)<br/>
                reach out to Josiah Leon, jleon@appacademy.io</i>
                </p>
            </body>
        </html>
        '''
            
        message.attach(MIMEText(text, 'plain'))
        message.attach(MIMEText(html, 'html'))
        
        server.sendmail(sender_email, receiver_email, message.as_string())
        
        
if __name__ == '__main__':
    em = Emailer()
    em.scan_sheets()