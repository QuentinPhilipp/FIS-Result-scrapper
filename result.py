from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException        

# import datetime
# import re
# import json
# from eventDate import EventDate
# import copy


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver',options=chrome_options)



class Result(object):
    """
    Represent an result of an event. PResults structur depend on the type
    """
    def __init__(self,url,raceType):
        self.url = url
        self.raceType = raceType
        


    def getResults(self):
        return "Results 1"