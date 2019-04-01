from collections import namedtuple
import json
from utils import config
import os

# Declare constant variables here

class WINDCHANGE(object):
    UP = "Up"
    DOWN = "Down"

    def __setattr__(self, *_):
        # Prevent from changing the class memebers values
        pass

class SOURCEREAD(object):
    PRIGAL = "Prigal"
    #EILAT_SURF_CENTER = "Eilat SurfCenter"
    EILAT_METEO_TECH = "Eilat MeteoTech"
    #NACHSHONIM = "Nachshonim"
    DOR_NACHSHOLIM = "Dor-Nachsholim"

    def __setattr__(self, *_):
        # Prevent from changing the class memebers values
        pass

class WINDDIFF(object):
    MIN_DIFF_ALERT = config.getint("winddiffs", "mindiffinterval")
    IMPORTANT_DIFF_ALERT = config.getint("winddiffs", "importantdiffinterval")
    MIN_ALERT = config.getint("winddiffs", "min_wind_strenght_alert")
    WIND_CHECK_INTERVAL = config.getint("winddiffs", "wind_check_interval")


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

class SECRETS(object):
    # Read the json containing the serets
    with open("secrests.json.secret") as json_data:
        data = json.load(json_data)    
        CHATID = data["wind_alert_group_chat_id"]
        BOTID = data["bot_token"]
    
    # CHATID = int(os.getenv("wind_alert_group_chat_id"))
    # BOTID = os.getenv("bot_token")
    
    @staticmethod
    def from_dict(source):
        # ...
        return namedtuple("SECRETS", source.keys())(*source.values())