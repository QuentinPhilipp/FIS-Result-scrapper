from competition import Competition
from event import Event
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


driver = webdriver.Chrome('/usr/bin/chromedriver',options=chrome_options)


url = "https://www.fis-ski.com/DB/alpine-skiing/calendar-results.html?eventselection=&place=&sectorcode=AL&seasoncode=2021&categorycode=WC&disciplinecode=&gendercode=&racedate=&racecodex=&nationcode=&seasonmonth=X-2021&saveselection=-1&seasonselection="

driver.get(url)
print("Main page loaded")

elems = driver.find_elements_by_class_name("table-row")

# only get the first
elems = elems[0:4]

competitionList = []

for e in elems:
    competition = Competition(e)
    competitionList.append(competition)


# For each competition, go to the corresponding page
for competition in competitionList:
    url = f"https://www.fis-ski.com/DB/general/event-details.html?sectorcode=AL&eventid={competition.id}"
    print("Check competition :",url)
    driver.get(url)
    events = driver.find_elements_by_xpath('//*[@id="eventdetailscontent"]/*')
    for e in events:
        event = Event(e,competition.startDate.year)
        competition.events.append(event)

print("\nCompetition list:")

for competition in competitionList :
    print(competition)

# print("Number of competitions:",len(elems))
