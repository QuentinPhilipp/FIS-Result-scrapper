from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException        

# import datetime
# import re
import json
# from eventDate import EventDate
import copy


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver',options=chrome_options)



class Result(object):
    """
    Represent an result of an event. Results structur depend on the type
    """
    def __init__(self,url,raceType):
        self.url = url
        self.raceType = raceType

        with open("config.json",'r') as config:
            data = json.load(config)
            self.struct = data["resultsStruct"][raceType]

    def getResults(self):
        # print(f"Load results for event : {self.url}")
        driver.get(self.url)
        # print("Results loaded")

        # Get size of the table

        fullTable = driver.find_elements_by_xpath('//*[@id="events-info-results"]/div/*')
        athleteCount = len(fullTable)


        # Check all athletes 
        for rank in range(1,athleteCount):
            # setattr(self,rank,None)
            # Get all elems according to the struct
            athleteResult = {}

            for elem in self.struct.keys():
                xPath = self.struct[elem]

                # replace {{rank}} in the xpath with the rank
                xPath = xPath.replace("{{rank}}",str(rank))
                # print(f"Elem {elem} at xPath : {xPath})")
                
                athleteResult[elem] = driver.find_element_by_xpath(xPath).get_attribute("innerHTML").strip()
        
            setattr(self,str(rank),athleteResult)

        copyObject = copy.copy(self)
        del copyObject.struct
        del copyObject.url
        del copyObject.raceType

        return copyObject.__dict__



if __name__ == "__main__":
    url = "https://www.fis-ski.com/DB/general/results.html?sectorcode=AL&raceid=104272"
    res = Result(url,"Giant Slalom")
    res.getResults()