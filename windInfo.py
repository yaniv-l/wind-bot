import datetime
from enum import Enum
import re
import json
from utils import config
import consts


class WindSpdUnit(Enum):
    KN = 'kn'
    KH = 'kh'
    MS = 'ms'

class windInfo:
    
    def __init__(self, sourceName, sourceURL, speedUnit = None, strengthSeperator = '-'):
        self._scrapTimeStamp = datetime.datetime.now().timestamp()
        self._scrapTimeStampStr = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._inputWindStrengthUnit = speedUnit or WindSpdUnit.KH
        self._windDir = None
        self._windDirName = None
        self._windAvg = None
        self._windGust = None
        self._windStrength = None
        self._infoDate = None
        self._infoTime = None
        self._infoSourceName = sourceName
        self._infoSourceURL = sourceURL
        self._infoImage = ""
        self._waterTemp = None
        self._Temp = None
        self._barometerPreasure = None
        self._strengthSeperator = strengthSeperator
        self._readAlerted = False
        self._windChanged = None

    # Utils functions

    def getWindDirName(self, windDir = None):
        windDirVal = windDir or self.windDir
        if windDirVal > 354.5 and windDirVal <= 5.625:
            return 'N'
        elif windDirVal > 5.625 and windDirVal <= 28.125:
            return 'NNE'
        elif windDirVal > 28.125 and windDirVal <= 50.625:
            return 'ENE'
        elif windDirVal > 50.625 and windDirVal <= 129.375:
            return 'E' 
        elif windDirVal > 129.375 and windDirVal <= 151.875:
            return 'SE'
        elif windDirVal > 151.875 and windDirVal <= 174.375:
            return 'ESE'
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
    
    
    def extractRegEx(self, extractorConfig, val):
        ''' This function will check if we have a config to extract data from the value
            if its a has, then uses regex to split the required data from the val using regex '''
        regex = config.get(self.infoSourceName, extractorConfig)
        if regex is None or not regex:
            return val
        else:
            extract = re.findall(regex, val)
            if extract:
                if len(extract[0]) > 0:
                    return extract[0][0]
                else:
                    return extract[0]
            else:
                return None
        

    def getDateTime(self, val):

        readDateTime = None
        datetimeVal = self.extractRegEx("datetimeExtractor", val)
        try:
            ''' Convert an input string to datetime based on the format string of the station '''
            dateTimeFormat = config.get(self.infoSourceName, "dateFormat") + " " + config.get(self.infoSourceName, "timeFormat")
            readDateTime = datetime.datetime.strptime(datetimeVal.strip(), dateTimeFormat.strip())
            # Check yead is datetime.minyear = input string did not include year. If so replace year to current year
            if readDateTime.year == 1900:
                readDateTime = readDateTime.replace(year=datetime.datetime.now().year)
        finally:
            return readDateTime

    def getKnots(self, value):
        if self._inputWindStrengthUnit == WindSpdUnit.MS.value:
            return round(float(value) * 1.94)
        elif self._inputWindStrengthUnit == WindSpdUnit.KH.value:
            return round(float(value) * 0.54)
        else:
            return value


    def getString(self, val, regex = '[A-z]{2,4}'):
        ''' This uses regex to split the number from the string characters to get the
            ie if val is 45NE then will return NE '''
        strVal = re.fullmatch(regex, val)
        if strVal:
            return strVal[0]
        else:
            return None

    def encode_complex(self, z):
        '''
        To translate a custom object into JSON, we need to provide an encoding function to the 
        dump() method’s default parameter. The json module will call this function on any objects that aren’t 
        natively serializable.
        '''
        if isinstance(z, WindSpdUnit):
            # if object is of type WindSpdUnits, we'll return the value
            return z.value
        else:
            type_name = z.__class__.__name__
            raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

    # def decode_complex(dct):
    #     if "__complex__" in dct:
    #         return complex(dct["real"], dct["imag"])
    #     return dct
    

    def toJSON(self, asString = False):
        j = json.dumps(self.__dict__, default=self.encode_complex, indent=4).encode()
        return j if asString else json.loads(j)

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

    @property
    def windAvg(self):
        return self._windAvg

    @windAvg.setter
    def windAvg(self, value):
        self._windAvg = self.getKnots(value)

    @property
    def windGust(self):
        return self._windGust

    @windGust.setter
    def windGust(self, value):
        self._windGust = self.getKnots(value)

    @property
    def windStrength(self):
        return self._windStrength

    @windStrength.setter
    def windStrength(self, value):
        self._windStrength = value
        if self.windAvg == None and self.windGust == None:
            strength = value.split(self._strengthSeperator)
            if  strength and strength.__len__() == 2:
                units = self.getString(strength[0])
                if units and units.upper() in WindSpdUnit.__members__:
                    self._inputWindStrengthUnit = WindSpdUnit[units.upper()]
                self._windAvg = self.getNumber(strength[0])
                self._windGust = self.getNumber(strength[1])


    @property
    def infoDate(self):
        return self._infoDate

    @infoDate.setter
    def infoDate(self, value):
        self._infoDate = value

    @property
    def infoTime(self):
        return self._infoTime

    @infoTime.setter
    def infoTime(self, value):
        self._infoTime = value

    @property
    def infoSourceName(self):
        return self._infoSourceName

    @infoSourceName.setter
    def infoSourceName(self, value):
        self._infoSourceName = value

    @property
    def infoSourceURL(self):
        return self._infoSourceURL

    @infoSourceURL.setter
    def infoSourceURL(self, value):
        self._infoSourceURL = value

    @property
    def infoImage(self):
        return self._infoImage

    @infoImage.setter
    def infoImage(self, value):
        self._infoImage = value

    @property
    def waterTemp(self):
        return self._waterTemp

    @waterTemp.setter
    def waterTemp(self, value):
        self._waterTemp = value

    @property
    def Temp(self):
        return self._Temp

    @Temp.setter
    def Temp(self, value):
        self._Temp = value

    @property
    def barometerPreasure(self):
        return self._barometerPreasure

    @barometerPreasure.setter
    def barometerPreasure(self, value):
        self._barometerPreasure = value

    @property
    def scrapTimeStamp(self):
        return self._scrapTimeStamp

    @property
    def strengthSeperator(self):
        return self._strengthSeperator
    
    @property
    def readDateTime(self):
        return str.format("{} {}", self.infoDate, self.infoTime)

    @readDateTime.setter
    def readDateTime(self, Value):
        readDateTime = self.getDateTime(Value)
        if readDateTime is not None:
            self.infoDate = readDateTime.strftime(config.get(self.infoSourceName, "dateFormat"))
            self.infoTime = readDateTime.strftime(config.get(self.infoSourceName, "timeFormat"))
        
    