import json
from collections import namedtuple
from windInfo import windInfo, WindSpdUnit

data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
data2 = '{"_infoTime" : "11:30", "_infoSourceName": "Prigal", "_infoSourceURL": "http://wind.co.il/#sea_state", "_infoImage": "", "_waterTemp": null, "_Temp": null, "_barometerPreasure": null, "_strengthSeperator": "-"}' 
# Parse JSON into an object with attributes corresponding to dict keys.
x = json.loads(data2, object_hook=lambda d: namedtuple('windInfo', (t.replace('_', '') for t in d.keys()))(*d.values()))
print(x.name, x.hometown.name, x.hometown.id)

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

p = namedtuple('Person', '_name _age _gender')
c = City(u'San Francisco', u'CA', u'USA', False, 860000).to_dict()
b = City.from_dict(c)
print(b)