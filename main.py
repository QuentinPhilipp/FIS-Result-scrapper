from competition import Competition
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


driver = webdriver.Chrome('/usr/bin/chromedriver',options=chrome_options)


url = "https://www.fis-ski.com/DB/alpine-skiing/calendar-results.html?eventselection=&place=&sectorcode=AL&seasoncode=2021&categorycode=WC&disciplinecode=&gendercode=&racedate=&racecodex=&nationcode=&seasonmonth=X-2021&saveselection=-1&seasonselection="

print(url)


driver.get(url)

elems = driver.find_elements_by_class_name("table-row")

# only get the 4 first

elems = elems[0:3]

competitionList = []

for e in elems:
    competition = Competition(e)
    competitionList.append(competition)


print(competitionList)

# print("Number of competitions:",len(elems))
