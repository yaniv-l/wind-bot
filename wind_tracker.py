from contextlib import suppress
import consts

def sense_for_wind_change(wind_reads):
    # This fuction will get a wind reads list and will process it to check for wind change
    # list assumption is that its ordered - position 0 is last read and position at len-1 is last
    if wind_reads:
        i_wind_avg_change = 0
        i_wind_gust_change = 0
        b_change_alerter = False
        # suppressing exception of type type convertion error and key missing errors
        with suppress(TypeError, KeyError):
            for i in range(len(wind_reads)):
                if i <= 2:
                    # Summing the change in the wing avg and gust in the in the last 3 reads
                    i_wind_avg_change += int(wind_reads[i][consts.WINDREADSFIELDS.WIND_AVG]) - int(wind_reads[0][consts.WINDREADSFIELDS.WIND_AVG])
                    i_wind_gust_change += int(wind_reads[i][consts.WINDREADSFIELDS.WIND_GUST]) - int(wind_reads[0][consts.WINDREADSFIELDS.WIND_GUST])
                if not b_change_alerter:
                    # Checking if a wind alert has been sent in the last reads perioed (default is last 6 reads)
                    b_change_alerter = wind_reads[i][consts.WINDREADSFIELDS.READ_ALERTED]
                pass
        
        if i_wind_avg_change > 0 and i_wind_avg_change <= consts.WINDDIFF.MIN_ALERT and i_wind_avg_change < consts.WINDDIFF.IMPORTANT_ALERT:
            pass
        elif i_wind_avg_change > 0 and i_wind_avg_change > consts.WINDDIFF.MIN_ALERT and i_wind_avg_change >= consts.WINDDIFF.IMPORTANT_ALERT:
            pass
        elif i_wind_avg_change < 0 and abs(i_wind_avg_change) <= consts.WINDDIFF.MIN_ALERT:
            pass
        elif i_wind_avg_change < 0 and abs(i_wind_avg_change) >= consts.WINDDIFF.IMPORTANT_ALERT:
            pass
        else:
            pass