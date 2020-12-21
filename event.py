from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException        

import datetime
import re
import json
from eventDate import EventDate
import copy


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver',options=chrome_options)



class Event(object):
    """
    Represent an Event. Potentially mutliple event in one competition.
    """
    def __init__(self,ref,year):
        self.ref = ref
        self.year = year

        try : 
            # Search if cancel 
            self.cancelled = ref.find_element_by_class_name("cancelled") != None

        except NoSuchElementException: 
            self.cancelled=False
    
        if not self.cancelled:
            self.date = self.getDate(ref)
            self.category = ref.find_element_by_xpath("./div/div[1]/div/a[3]/div/div/div/div").get_attribute("innerHTML").strip()
            self.resultsHREF = ref.find_element_by_xpath("./div/div[1]/div/a[1]").get_attribute("href")
        else:
            self.date=None
            self.category=None
            self.resultsHREF=None


    def getDate(self,ref):
        eventDateRaw = ref.find_element_by_xpath("./div/div[1]/div/a[2]/div/div/div").get_attribute("innerHTML")
        eventHourRaw = ref.find_element_by_xpath("./div/div[1]/div/a[7]/div/div[1]/div/div[2]").get_attribute("innerHTML")

        strDate = str(self.year)+" "+eventDateRaw+"-"+eventHourRaw
        eventDate = datetime.datetime.strptime(strDate,"%Y %d %b-%H:%M")

        return eventDate


    def __repr__(self):
        objDict = copy.copy(self).__dict__

        del objDict["ref"]
        del objDict["date"]
        del objDict["year"]

        if self.date != None:
            objDict['date'] = EventDate(self.year,self.date.month,self.date.day,self.date.hour,self.date.minute).__dict__
        else :
            objDict['date'] = EventDate().__dict__

        return json.dumps(objDict)


    def __str__(self):
        if self.cancelled:
            return "Cancelled"
        else:
            return self.category+" : "+str(self.date)+ " -> "+self.resultsHREF



    def customDict(self):
        objDict = copy.copy(self).__dict__

        del objDict["ref"]
        del objDict["date"]
        del objDict["year"]

        if self.date != None:
            objDict['date'] = EventDate(self.year,self.date.month,self.date.day,self.date.hour,self.date.minute).__dict__
        else :
            objDict['date'] = EventDate().__dict__

        return objDict

