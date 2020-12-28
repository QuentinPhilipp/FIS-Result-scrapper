from operator import attrgetter

class Country(object):
    """
    Represent the number of podium from a country
    """
    def __init__(self,name):
        self.name = name
        self.first = 0
        self.second = 0
        self.third = 0

    def increaseCounter(self,result=-1):
        if result==0:
            self.first+=1
        elif result==1:
            self.second+=1
        elif result==2:
            self.third+=1


    def __repr__(self):
        return f" {self.name} - {self.first} | {self.second} | {self.third}"

def countryPodiumTable(data,raceType):
    podium = []
    for competition in data:
        for event in competition["events"]:
            if event["cancelled"]==False and event["review"]==True:
                if event["type"]==raceType or raceType=="All":
                    # Get the data from 1st to 3rd place
                    results = []
                    results.append(event["results"]['1']["nation"])
                    results.append(event["results"]['2']["nation"])
                    results.append(event["results"]['3']["nation"])

                    # If not in the podium list, create a new country to add in the list
                    # Else increase the counters
                    # print(results)
                    for i,result in enumerate(results):
                        for country in podium:
                            if country.name == result:
                                country.increaseCounter(i)     
                                break               
                        else:
                            newCountry = Country(result)
                            newCountry.increaseCounter(i)
                            podium.append(newCountry)

    # Sort the podium 
    podium = sorted(podium, key = attrgetter('first','second','third'),reverse=True)

    # for country in podium:
    #     print(country)
    return podium








if __name__ == "__main__":
    import json

    with open("results.json","r") as results:
        res = json.load(results)

        countryPodiumTable(res,"All")