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
        pass
    
    def __init__(self) -> None:
        # setting up firebase connection
        cred = credentials.Certificate(FIRESTORE_CRED)
        self.app = firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        
        # getting data to upload
        self.__get_most_recent_json()
        
    def upload_data(self) -> None:
        coll = self.db.collection('healthData')
        data = None
        # turn self.json into dict via the data var
    
    def test_read(self):
        items = self.db.collection('healthData')
        docs = items.stream()
        
        for doc in docs:
            print(doc.id, doc.to_dict())
    
if __name__ == '__main__':
    # raise Exception('uploader is not ran directly, it must be imported to be used!')
    up = Uploader()