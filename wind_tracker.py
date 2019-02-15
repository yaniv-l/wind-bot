from contextlib import suppress
import consts
import telegram_bot
import firedata
from datetime import datetime, time
from enum import IntFlag

from utils import config

class WindTrend(IntFlag):
    INCREASE = 1
    DECREASE = 2
    STEADY = 0


strings_dict = {
        WindTrend.INCREASE : {"name": "Increase", "change": "UP", "label": "עליה"},
        WindTrend.DECREASE : {"name": "decrease", "change": "down", "label": "ירידה"},
        True : {"name": "consistant", "change": "", "label": "רציפה"},
        False : {"name": "comulative", "change": "", "label": "מצטברת"}
}


def sense_for_wind_change(wind_reads):
    # This fuction will get a wind reads list and will process it to check for wind change
    # list assumption is that its ordered - position 0 is last read and position at len-1 is last
    if wind_reads:
        i_wind_avg_change = 0
        i_wind_gust_change = 0
        b_change_alerter = False
        str_trend = None
        str_UpDown = None
        str_windChange = None
        i_changeTrend = None
        b_changeTrendConsistant = True
        
        # suppressing exception of type type convertion error and key missing errors
        with suppress(TypeError, KeyError):
            for i in range(1, len(wind_reads)-1):
                if i <= 3:
                    # Summing the change in the wing avg and gust in the in the last 3 reads
                    i_wind_avg_change += wind_reads[i-1][consts.WINDREADSFIELDS.WIND_AVG] - wind_reads[i][consts.WINDREADSFIELDS.WIND_AVG]
                    i_wind_gust_change += wind_reads[i-1][consts.WINDREADSFIELDS.WIND_AVG] - wind_reads[i][consts.WINDREADSFIELDS.WIND_GUST]
                    trend = getChangeTrend(wind_reads[i-1][consts.WINDREADSFIELDS.WIND_AVG], wind_reads[i][consts.WINDREADSFIELDS.WIND_AVG])
                    # Accumalating the mins on which the change trend is based on
                    i_wind_trend_duration += consts.WINDDIFF.WIND_CHECK_INTERVAL
                    # set the i_changeTrend for the first itrerate, and we'll check following itterare if they match
                    # same initial trend to conclude it is consistant 
                    if i_changeTrend is None:
                        i_changeTrend = trend
                    else:
                        if b_changeTrendConsistant:
                            #b_changeTrendConsistant = i_changeTrend == trend
                            # Check if last tred match the initial trend - if not trend is not consistant and set b_changeTrendConsistant to False
                            b_changeTrendConsistant = bool(i_changeTrend & trend)
                if not b_change_alerter:
                    # Checking if a wind alert has been sent in the last reads perioed (default is last 6 reads)
                    b_change_alerter = wind_reads[i][consts.WINDREADSFIELDS.READ_ALERTED]
                pass
        # TODO - Review the sense check (if blocks)
        if wind_reads[0][consts.WINDREADSFIELDS.WIND_AVG] >= consts.WINDDIFF.MIN_ALERT:    
            if i_wind_avg_change > 0 and i_wind_avg_change <= consts.WINDDIFF.MIN_DIFF_ALERT and i_wind_avg_change < consts.WINDDIFF.IMPORTANT_DIFF_ALERT and not b_change_alerter:
                str_trend = "*עליה*"
                str_UpDown = "עלתה ב "
                str_windChange = consts.WINDCHANGE.UP
            elif i_wind_avg_change > 0 and i_wind_avg_change > consts.WINDDIFF.MIN_ALERT and i_wind_avg_change >= consts.WINDDIFF.IMPORTANT_DIFF_ALERT:
                str_trend = "*עליה חזקה*"
                str_UpDown = "*התגברה ב*"
                str_windChange = consts.WINDCHANGE.UP
            elif i_wind_avg_change < 0 and abs(i_wind_avg_change) >= consts.WINDDIFF.MIN_ALERT and abs(i_wind_avg_change) < consts.WINDDIFF.IMPORTANT_DIFF_ALERT and not b_change_alerter:
                str_trend = "*ירידה*"
                str_UpDown = "ירדה ב"
                str_windChange = consts.WINDCHANGE.DOWN
            elif i_wind_avg_change < 0 and abs(i_wind_avg_change) >= consts.WINDDIFF.IMPORTANT_DIFF_ALERT:
                str_trend = "*ירידה*"
                str_UpDown = "ירדה ב"
                str_windChange = consts.WINDCHANGE.DOWN
            else:
                pass
        
        if isAlertTime() and str_trend is not None and str_UpDown is not None:
            # Formating alert messgae
            alert_message = str.format("_הי, הרוח נושבת קרירה, נוסיף עוד קשר למפרש..._\n רוח במגמת {} - {} {}kn בחצי שעה האחרונה.\n כרגע {}kn עם גאסטים של {}kn\nכיוון {}, {}\nזמן קריאה {} {}\nמקור [{}]({})", \
                str_trend, str_UpDown, i_wind_avg_change, wind_reads[0][consts.WINDREADSFIELDS.WIND_AVG], wind_reads[0][consts.WINDREADSFIELDS.WIND_GUST], wind_reads[0][consts.WINDREADSFIELDS.WIND_DIR], \
                wind_reads[0][consts.WINDREADSFIELDS.WIND_DIR_NAME], wind_reads[0][consts.WINDREADSFIELDS.INFO_DATE], wind_reads[0][consts.WINDREADSFIELDS.INFO_TIME], wind_reads[0][consts.WINDREADSFIELDS.INFO_SOURCE_NAME], \
                wind_reads[0][consts.WINDREADSFIELDS.INFO_SOURCE_URL])
            # Sending wind alert to telegram chat group
            telegram_bot.sendWindAlert(alert_message)
            # Updating wind read for alert sent
            firedata.setWindAlert(wind_reads[0][consts.WINDREADSFIELDS.DOC_ID], str_windChange)


def isAlertTime():
    alertFrom = datetime.strptime(config.get("alerttimewindow", "fromtime"), "%H:%M").time()
    alertTill = datetime.strptime(config.get("alerttimewindow", "totime"), "%H:%M").time()
    now = datetime.now().time()
    return now >=  alertFrom and now < alertTill

def getChangeTrend(current, prev):
    ret = None
    if current > prev:
        ret = WindTrend.INCREASE
    elif current < prev:
        ret = WindTrend.DECREASE
    else:
        ret = WindTrend.STEADY
    return ret
            