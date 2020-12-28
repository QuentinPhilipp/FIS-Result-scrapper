from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException        

import datetime
import re
import json
from eventDate import EventDate
from result import Result
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

        #check if live or already finished : 
        try : 
            self.review = ref.find_element_by_class_name("live__content") != None
        except NoSuchElementException: 
            self.review=False
    
        if not self.cancelled:
            if self.review:
                self.type = ref.find_element_by_xpath("./div/div[1]/div/a[3]/div/div/div/div").get_attribute("innerHTML").strip()
                self.category = ref.find_element_by_xpath('./div/div[1]/div/a[5]').get_attribute("innerHTML").strip()
                self.resultsHREF = ref.find_element_by_xpath("./div/div[1]/div/a[1]").get_attribute("href")
            else : 
                self.type = ref.find_element_by_xpath("./div/div[1]/div/a[4]/div/div/div/div").get_attribute("innerHTML").strip()
                self.category = ref.find_element_by_xpath('./div/div[1]/div/a[6]').get_attribute("innerHTML").strip()
        else :
            self.type = ref.find_element_by_xpath("./div/div[1]/div/a[4]/div/div/div/div").get_attribute("innerHTML").strip()
            self.category = ref.find_element_by_xpath('./div/div[1]/div/a[6]').get_attribute("innerHTML").strip()            
        
        self.date = self.getDate(ref)

        self.results = self.getResults()


    def getDate(self,ref):

        # No hours for training sessions
        if self.category!="TRA":
            if self.review:
                eventHourRaw = ref.find_element_by_xpath("./div/div[1]/div/a[7]/div/div[1]/div/div[2]").get_attribute("innerHTML")
            else:
                eventHourRaw = ref.find_element_by_xpath("./div/div[1]/div/a[8]/div/div[1]/div/div[2]").get_attribute("innerHTML")
        else:
            eventHourRaw = "00:00"

        eventDateRaw = ref.find_element_by_xpath("./div/div[1]/div/a[2]/div/div/div").get_attribute("innerHTML")

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




    def getResults(self):

        if not self.cancelled and self.review:
            resultsObj = Result(self.resultsHREF,self.type)
            results = resultsObj.getResults()
        else :
            results="None"

        return results



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






if __name__ == "__main__":
    # url = "https://www.fis-ski.com/DB/general/event-details.html?sectorcode=AL&eventid=46945"
    # url = "https://www.fis-ski.com/DB/general/event-details.html?sectorcode=AL&eventid=46965&seasoncode=2021"
    url = "https://www.fis-ski.com/DB/general/event-details.html?sectorcode=AL&eventid=46935&seasoncode=2021"
    driver.get(url)
    elems = driver.find_elements_by_xpath('//*[@id="eventdetailscontent"]/*')
    print("Event page loaded")


    elems = elems[0:1]

    eventList = []

    for elem in elems:
        event = Event(elem,2020)
        eventList.append(event)

    print(eventList)
