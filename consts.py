# Declare constant variables here

class WINDCHANGE(object):
    UP = "Up"
    DOWN = "Down"

    def __setattr__(self, *_):
        # Prevent from changing the class memebers values
        pass

class SOURCEREAD(object):
    PRIGAL = "Prigal"
    EILAT_SURF_CENTER = "Eilat SurfCenter"
    EILAT_METEO_TECH = "Eilat MeteoTech"
    NACHSHONIM = "Nachshonim"

    def __setattr__(self, *_):
        # Prevent from changing the class memebers values
        pass

class WINDDIFF(object):
    MIN_ALERT = 1
    IMPORTANT_ALERT = 3

    def __setattr__(self, *_):
        # Prevent from changing the class memebers values
        pass

class WINDREADSFIELDS(object):
    SCRAP_TIMESTAMP = "_scrapTimeStamp"
    SCRAP_TIMESTAMP_STR = "_scrapTimeStampStr"
    WIND_STRENGTH_UNIT = "_inputWindStrengthUnit"
    WIND_DIR = "_windDir"
    WIND_DIR_NAME = "_windDirName"
    WIND_AVG = "_windAvg"
    WIND_GUST = "_windGust"
    WIND_STRENGTH = "_windStrength"
    INFO_DATE = "_infoDate"
    INFO_TIME = "_infoTime"
    INFO_SOURCE_NAME = "_infoSourceName"
    INFO_SOURCE_URL = "_infoSourceURL"
    INFO_IMAGE = "_infoImage"
    WATER_TEMP = "_waterTemp"
    TEMP = "_Temp"
    BAROMETER_PREASURE = "_barometerPreasure"
    STRENGTH_SEPERATOR = "_strengthSeperator"
    READ_ALERTED = "_readAlerted"
    WIND_CHANGED = "_windChanged"
    DOC_ID = "_id"

    def __setattr__(self, *_):
        # Prevent from changing the class memebers values
        pass