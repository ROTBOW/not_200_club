import requests
import os


urls = [
    'https://all-bnb.herokuapp.com/',
    'https://mtg-spark.herokuapp.com/',
    'https://rebuildable.herokuapp.com/',
    'http://sketchcircle.herokuapp.com/'
    ]



for url in urls:
    res = requests.get(url)
    print(res.status_code)
    print(res.elapsed)
    print()