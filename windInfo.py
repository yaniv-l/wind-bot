from enum import Enum
import re

class WindSpdUnit(Enum):
    KN = 'kn'
    KH = 'kh'
    MS = 'ms'

class windInfo:
    
    def __init__(self, sourceName, sourceURL, speedUnit = None):
        self._inputWindStrengthUnit = speedUnit or WindSpdUnit.KH
        self._windDir = -1
        self._windDirName = None
        self._windAvg = 0
        self._windGust = 0
        self._windStrength = ""
        self._infoDate = None
        self._infoTime = None
        self._infoSourceName = sourceName
        self._infoSourceURL = sourceURL
        self._infoImage = ""
        self._waterTemp = -1
        self._Temp = -1

    # Utils functions

    def getWindDirName(self, windDir = None):
        windDirVal = windDir or self.windDir
        if windDirVal > 354.5 and windDirVal <= 5.625:
            return 'N'
        elif windDirVal > 5.625 and windDirVal <= 28.125:
            return 'NNE'
        elif windDirVal > 28.125 and windDirVal <= 50.625:
            return 'NNE'
        elif windDirVal > 50.625 and windDirVal <= 129.375:
            return 'E' 
        elif windDirVal > 129.375 and windDirVal <= 151.875:
            return 'SE'
        elif windDirVal > 151.875 and windDirVal <= 174.375:
            return 'SSE'
        elif windDirVal > 174.375 and windDirVal <= 196.875:
            return 'S'
        elif windDirVal > 196.875 and windDirVal <= 219.375:
            return 'SSW'
        elif windDirVal > 219.375 and windDirVal <= 241.875:
            return 'SW'
        elif windDirVal > 241.875 and windDirVal <= 264.375:
            return 'WSW'
        elif windDirVal > 264.375 and windDirVal <= 286.875:
            return 'W'
        elif windDirVal > 286.875 and windDirVal <= 309.375:
            return 'WNW'
        elif windDirVal > 309.375 and windDirVal <= 331.875:
            return 'NW'
        elif windDirVal > 331.875 and windDirVal <= 354.375:
            return 'NNW'
        else:
            return 'n/a'
    
    def getNumber(self, val):
        ''' This function will check the type of the val
            if its a string type then uses regex to split the number from the string characters
            ie if val is 45NE then will return 45 '''
        valtype = type(val)
        if valtype is int or valtype is float:
            return val
        elif valtype is str:
            num = re.findall('\d+', val)
            if num:
                return num[0]
            else:
                return None
        else:
            raise Exception('Error while getNumber from content {}'.format(val))

    def getString(self, val, regex = '[A-z]{2,4}'):
        ''' This uses regex to split the number from the string characters to get the
            ie if val is 45NE then will return NE '''
        strVal = re.findall(regex, val)
        if strVal:
            return strVal[0]
        else:
            return None
    
    # Properties - setters and getters

    @property
    def windDir(self):
        return self._windDir

    @windDir.setter
    def windDir(self, value):
        # value can contain also wind direction name characters
        dirVal = int(self.getNumber(value))
        self._windDir = dirVal
        if self.windDirName == None:
            self.windDirName = self.getString(value) or self.getWindDirName()
    
    @property
    def windDirName(self):
        return self._windDirName

    @windDirName.setter
    def windDirName(self, value):
        self._windDirName = value