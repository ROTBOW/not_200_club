import os

from dotenv import load_dotenv

# loading the local .env file
load_dotenv()

print(os.environ.get('josiah_leon'))