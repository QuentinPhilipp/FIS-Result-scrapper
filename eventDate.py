import json

class EventDate(object):
    """
    Custom class to store the dates of an event. Easy to serialize for storage
    """
    def __init__(self,year=1970,month=1,day=1,hour=0,min=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.min = min

    def getJson(self):
        """
        Return a serialized version of the date
        """
        return json.dumps(self.__dict__)