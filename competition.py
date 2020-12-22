from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException        

import datetime
import re
import json
import copy
from eventDate import EventDate


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver',options=chrome_options)



class Competition(object):
    """
    Represent a competition item
    """
    def __init__(self,ref):
        self.ref = ref
        self.id = ref.get_attribute("id")
        self.setDate(ref)
        self.events = []


    def setDate(self,ref):

        try : 
            # Search if live 
            self.live = ref.find_element_by_class_name("live") != None
        except NoSuchElementException: 
            self.live=False

        # If live competition, the index is different 
        if self.live:
            eventDateRaw = ref.find_element_by_xpath("./div/div/a[3]").get_attribute("innerHTML")
        else:
            eventDateRaw = ref.find_element_by_xpath("./div/div/a[2]").get_attribute("innerHTML")
        

        #Use a bit of regex magic to get startDate, endDate, month and year.
        # ^(\w+)\s+(\w+)\s+(\w+)$  -> One day event
        test1 = r"^(\w+)\s+(\w+)\s+(\w+)$"
        result1 = re.findall(test1,eventDateRaw)

        # (\w+)-(\w+)\s+(\w+)\s+(\w+)$  -> Multiple days
        test2 = r"(\w+)-(\w+)\s+(\w+)\s+(\w+)$"
        result2 = re.findall(test2,eventDateRaw)

        if len(result1)>0:
            result = result1[0]
            startDay = result[0]
            endDay = result[0]
            monthStr = result[1]
            year = result[2]

        elif len(result2)>0:
            result = result2[0]
            startDay = result[0]
            endDay = result[1]
            monthStr = result[2]
            year = result[3]

        else:
            print("Error parsing date")


        # Convert string date to number
        with open("config.json") as f:
            data=json.load(f)
            month = data["month"][monthStr]

        self.startDate = datetime.date(int(year),int(month),int(startDay))
        self.endDate = datetime.date(int(year),int(month),int(endDay))


    def __repr__(self):
        objDict = copy.copy(self).__dict__

        del objDict["ref"]
        del objDict["startDate"]
        del objDict["endDate"]

        objDict['startDate'] = EventDate(self.startDate.year,self.startDate.month,self.startDate.day).__dict__
        objDict['endDate'] = EventDate(self.endDate.year,self.endDate.month,self.endDate.day).__dict__

        return json.dumps(objDict)

    def __str__(self):
        dispString = "Competition "+str(self.id)+ " -> " +str(self.startDate.day)+ "-" + str(self.endDate.day) +" "+self.startDate.strftime("%b %Y")
        
        for event in self.events:    
            dispString += "\n  ~ " + str(event)
        return dispString


    def customDict(self):
        """
        Return a dict with nested events
        """
        objDict = copy.copy(self).__dict__

        del objDict["ref"]
        del objDict["startDate"]
        del objDict["endDate"]
        del objDict["events"]

        objDict['startDate'] = EventDate(self.startDate.year,self.startDate.month,self.startDate.day).__dict__
        objDict['endDate'] = EventDate(self.endDate.year,self.endDate.month,self.endDate.day).__dict__
        objDict["events"] = []
        for event in self.events:
            objDict["events"].append(event.customDict())
        return objDict


if __name__ == "__main__":
    url = "https://www.fis-ski.com/DB/alpine-skiing/calendar-results.html?eventselection=&place=&sectorcode=AL&seasoncode=2021&categorycode=WC&disciplinecode=&gendercode=&racedate=&racecodex=&nationcode=&seasonmonth=X-2021&saveselection=-1&seasonselection="
    driver.get(url)

    elems = driver.find_elements_by_class_name("table-row")

    # only get the 4 first

    elems = elems[0:3]

    competitionList = []

    for e in elems:
        competition = Competition(e)
        competitionList.append(competition)


    print(competitionList)
