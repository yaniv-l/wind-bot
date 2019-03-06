from contextlib import suppress
import consts
import telegram_bot
import firedata
from datetime import datetime, time
from enum import IntEnum

from utils import config

class WindTrend(IntEnum):
    INCREASE = 1
    DECREASE = 2
    STEADY = 0


strings_dict = {
        WindTrend.INCREASE.name : {"name": "Increase", "change": "UP", "label": "עליה", "verb": "עלתה"},
        WindTrend.DECREASE.name : {"name": "Decrease", "change": "DOWN", "label": "ירידה", "verb": "ירדה"},
        WindTrend.STEADY.name : {"name": "Steady", "change": "STEADY", "label": "יציבה", "verb": ""},
        True : {"name": "consistant", "change": "", "label": "רציפה", "verb": "*"},
        False : {"name": "comulative", "change": "", "label": "מצטברת", "verb": ""}
}


def sense_for_wind_change(wind_reads):
    # This fuction will get a wind reads list and will process it to check for wind change
    # list assumption is that its ordered - position 0 is last read and position at len-1 is last
    if wind_reads:
        # Make sure we have atleast two reads so to see a change
        if len(wind_reads) >= 2:
            # Make sure last read is not actually from last read (ocaisionly the wind reads are stuck for long time)
            if (wind_reads[0][consts.WINDREADSFIELDS.INFO_DATE] + " " + wind_reads[0][consts.WINDREADSFIELDS.INFO_TIME]) != (wind_reads[1][consts.WINDREADSFIELDS.INFO_DATE] + " " + wind_reads[1][consts.WINDREADSFIELDS.INFO_TIME]):
                i_wind_avg_change = 0
                i_wind_gust_change = 0
                b_change_alerter = False
                b_changeTrendConsistant = True
                i_wind_trend_duration = 0
                e_changeTrend = None
                
                # suppressing exception of type type convertion error and key missing errors
                with suppress(TypeError, KeyError):
                    for i in range(1, len(wind_reads)-1):
                        if i <= 3:
                            # Summing the change in the wing avg and gust in the in the last 3 reads
                            i_wind_avg_change += int(wind_reads[i-1][consts.WINDREADSFIELDS.WIND_AVG]) - int(wind_reads[i][consts.WINDREADSFIELDS.WIND_AVG])
                            i_wind_gust_change += int(wind_reads[i-1][consts.WINDREADSFIELDS.WIND_AVG]) - int(wind_reads[i][consts.WINDREADSFIELDS.WIND_GUST])
                            trend = getChangeTrend(int(wind_reads[i-1][consts.WINDREADSFIELDS.WIND_AVG]), int(wind_reads[i][consts.WINDREADSFIELDS.WIND_AVG]))
                            # Accumalating the mins on which the change trend is based on
                            i_wind_trend_duration += int(consts.WINDDIFF.WIND_CHECK_INTERVAL)
                            # set the e_changeTrend for the first itrerate, and we'll check following itterare if they match
                            # same initial trend to conclude it is consistant 
                            if e_changeTrend is None:
                                e_changeTrend = trend
                            else:
                                if b_changeTrendConsistant:
                                    #b_changeTrendConsistant = i_changeTrend == trend
                                    # Check if last tred match the initial trend - if not trend is not consistant and set b_changeTrendConsistant to False
                                    b_changeTrendConsistant = bool(e_changeTrend & trend)
                        if not b_change_alerter:
                            # Checking if a wind alert has been sent in the last reads perioed (default is last 6 reads)
                            b_change_alerter = wind_reads[i][consts.WINDREADSFIELDS.READ_ALERTED]
                        pass
                
                if isChangeForAlert(int(wind_reads[0][consts.WINDREADSFIELDS.WIND_AVG]), i_wind_avg_change, b_change_alerter) and isAlertTime():
                    # Formating alert messgae
                    sendWIndAlert(wind_reads[0], e_changeTrend,  b_changeTrendConsistant, i_wind_avg_change, i_wind_trend_duration, strings_dict[e_changeTrend.name]["change"])


def isChangeForAlert(current_wind, wind_avg_change, change_alerter):
    ret = False
    if current_wind >= consts.WINDDIFF.MIN_ALERT:
        # Wind is above min alert and no alert has been sent in the last processed wind reads
        if not change_alerter:
            ret = True
        # Alert has been sent in the last processed wind reads but winds has increased significantly
        # using abs(wind_avg_change) as change may be up or down - purpose here is to check if change is significant and requires an alert
        elif abs(wind_avg_change) >= consts.WINDDIFF.IMPORTANT_DIFF_ALERT:
            ret = True
        else:
            pass
        # TODO add more condition to find if current wind is lower then min alert and last alerted read
    
    return ret


def isAlertTime():
    alertFrom = datetime.strptime(config.get("alerttimewindow", "fromtime"), "%H:%M").time()
    alertTill = datetime.strptime(config.get("alerttimewindow", "totime"), "%H:%M").time()
    now = datetime.now().time()
    return now >=  alertFrom and now < alertTill

def sendWIndAlert(read, eTrend, bIsConssitant, wind_change, change_time, windChangeName):
    # Sending wind alert to telegram chat group
    telegram_bot.sendWindAlert(getAlertMessage(read, eTrend, bIsConssitant, wind_change, change_time), read[consts.WINDREADSFIELDS.INFO_SOURCE_NAME])
    # Updating wind read for alert sent
    firedata.setWindAlert(read[consts.WINDREADSFIELDS.DOC_ID], windChangeName)

def getAlertMessage(read, eTrend, bIsConssitant, wind_change, change_time):
    str_verb = strings_dict[eTrend.name]["verb"]
    str_trend = strings_dict[eTrend.name]["label"] + (" " + strings_dict[bIsConssitant]["label"] if eTrend != WindTrend.STEADY else "")
    str_sub_message = str.format("{verb} בכ {change}kn ", verb=str_verb, change=wind_change) if eTrend != WindTrend.STEADY else ""
    str_meaasge = str.format("{beach} - {trend}: {current}kn - {gust}kn {direction_name}-{direction}\n" + \
                            "{sub_message}ב {change_time} דקות האחרונות\n" + \
                            "זמן קריאה: {read_date} {read_time}\n" + \
                            "מקור [{source}]({source_url})", \
                            beach=config.get(read[consts.WINDREADSFIELDS.INFO_SOURCE_NAME], "beachName"), \
                            current=read[consts.WINDREADSFIELDS.WIND_AVG], \
                            gust=read[consts.WINDREADSFIELDS.WIND_GUST], \
                            direction_name=read[consts.WINDREADSFIELDS.WIND_DIR_NAME], \
                            direction=read[consts.WINDREADSFIELDS.WIND_DIR], \
                            trend=str_trend, \
                            sub_message=str_sub_message, \
                            verb=str_verb, \
                            change=wind_change,
                            change_time=change_time, \
                            read_date=read[consts.WINDREADSFIELDS.INFO_DATE], \
                            read_time=read[consts.WINDREADSFIELDS.INFO_TIME], \
                            source=config.get(read[consts.WINDREADSFIELDS.INFO_SOURCE_NAME], "frindlyName"), \
                            source_url=read[consts.WINDREADSFIELDS.INFO_SOURCE_URL])
    return str_meaasge


def getChangeTrend(current, prev):
    ret = None
    if current > prev:
        ret = WindTrend.INCREASE
    elif current < prev:
        ret = WindTrend.DECREASE
    else:
        ret = WindTrend.STEADY
    return ret
            