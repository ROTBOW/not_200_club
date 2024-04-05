'''
This is script is ran by the n2c script on completion to upload the most recent json file
to firestore for the frontend.
'''

import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# loading the local .env file
load_dotenv()

# Constants
DIR = os.path.dirname(os.path.realpath(__file__))
RES = os.path.join(DIR, 'res')
FIRESTORE_CRED = json.loads(os.getenv("FIREBASE_CRED"))


class Uploader:
    
    def __get_most_recent_json(self) -> None:
        """
        This Python function finds the most recent JSON file in a directory and sets the file path.
        """
        files = os.listdir(RES)
        most_recent_file = [0, '']
        
        for f in files:
            t = os.path.getmtime(os.path.join(RES, f))
            if f.endswith('json') and t > most_recent_file[0]:
                most_recent_file = [t, f]
        
        self.file_path = os.path.join(RES, most_recent_file[1])
    
    def __init__(self) -> None:
        # setting up firebase connection
        cred = credentials.Certificate(FIRESTORE_CRED)
        self.app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        
        # getting data to upload
        self.file_path = ''
        self.__get_most_recent_json()
        
    def upload_data(self) -> None:
        """
        The `upload_data` function reads JSON data from a file and adds it to a collection in a
        database.
        """
        coll = self.db.collection('healthData')
        data = None
        
        # turn self.json into dict via the data var
        with open(self.file_path, 'r') as f:
            data = json.loads(f.read())
            
        coll.add(data)
        print('data sent!')
    
if __name__ == '__main__':
    raise Exception('uploader is not ran directly, it must be imported to be used!')
    # up = Uploader()
    # up.upload_data()