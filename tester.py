import json
from collections import namedtuple
from windInfo import windInfo, WindSpdUnit
from utils import config
import consts
import datetime
from enum import IntFlag, Enum

data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
data2 = '{"_infoTime" : "11:30", "_infoSourceName": "Prigal", "_infoSourceURL": "http://wind.co.il/#sea_state", "_infoImage": "", "_waterTemp": null, "_Temp": null, "_barometerPreasure": null, "_strengthSeperator": "-"}' 
# Parse JSON into an object with attributes corresponding to dict keys.
# x = json.loads(data2, object_hook=lambda d: namedtuple('windInfo', (t.replace('_', '') for t in d.keys()))(*d.values()))
# print(x.name, x.hometown.name, x.hometown.id)

class City(object):
    def __init__(self, name, state, country, capital=False, population=0):
        self.name = name
        self.state = state
        self.country = country
        self.capital = capital
        self.population = population

    @staticmethod
    def from_dict(source):
        # ...
        return namedtuple("City", source.keys())(*source.values())

    def to_dict(self):
        # ...
        return self.__dict__

    def __repr__(self):
        return u'City(name={}, country={}, population={}, capital={})'.format(
            self.name, self.country, self.population, self.capital)

def getDateTime(val):
        
        ''' This function will check the type of the val
            if its a string type then uses regex to split the time from the string characters
            ie if val is 01/02 09:20 then will return 09:20 '''
        val.strip
        dateTimeFormat = config.get(consts.SOURCEREAD.EILAT_METEO_TECH, "dateFormat") + " " + config.get(consts.SOURCEREAD.EILAT_METEO_TECH, "timeFormat")
        readDateTime = datetime.datetime.strptime(val.strip(), dateTimeFormat)
        if readDateTime.year == 1900:
            readDateTime = readDateTime.replace(year=datetime.datetime.now().year)
        return readDateTime

def getChangeTrend(current, prev):
    ret = None
    if current > prev:
        ret = 1
    elif current < prev:
        ret = -1
    else:
        ret = 0
    return ret

# p = namedtuple('Person', '_name _age _gender')
# c = City(u'San Francisco', u'CA', u'USA', False, 860000).to_dict()
# b = City.from_dict(c)
print(getDateTime(" 01/02 10:20  "))
# numbres=[1.10, 1.25, 1.48, 1.5, 1.51, 1.8, 2, 2.1, 2.5, 2.51]
# for number in numbres:
#     print (str(number) + " --> " + str(round(number)))

class WindTrend(IntFlag):
    INCREASE = 1
    DECREASE = 2
    STEADY = 0

defs = {
        WindTrend.INCREASE : {"name": "increase", "change": "up", "label": "עליה"},
        WindTrend.DECREASE : {"name": "decrease", "change": "down", "label": "ירידה"},
        True : {"name": "increase", "change": "up", "label": "רציפה"}
}

# print(getChangeTrend(2,1))
# print(getChangeTrend(1,2))
# print(getChangeTrend(2,2))
# print(bool(WindTrend.DECREASE & WindTrend.INCREASE))
# print(bool(WindTrend.DECREASE & WindTrend.DECREASE))
# print(bool(WindTrend.INCREASE & WindTrend.INCREASE))
# print(bool(WindTrend.STEADY & WindTrend.STEADY))
# print(bool(WindTrend.INCREASE & WindTrend.STEADY))

a = defs[True]["label"]
print (a)




