import os
import sys
import re
from datetime import datetime

# configparser module was changed to ConfigParser in python 3 - check which runtime version to and load correct module for version
if sys.version_info[0] < 3:
    from ConfigParser import SafeConfigParser
else:
    from configparser import SafeConfigParser

# Init config
config = SafeConfigParser()
# Read the config file - if file cannot be found in the script dir, then assert.
assert (config.read(os.path.dirname(__file__) + "/wind-bot.cfg"))

def getMinDiff(datetimeFrom, datetimeTo):
    dateDiff = datetimeFrom - datetimeTo
    minDiff = (int(dateDiff.days) * 24 * 60) + int((dateDiff.seconds) / 60 )
    return minDiff

def extractRegEx(extractorConfig, val):
    ''' This function uses regex to split the required data from the val using regex '''
    extract = re.findall(extractorConfig, val)
    if extract:
        if len(extract[0]) > 0:
            return extract[0][0]
        else:
            return extract[0]
    else:
        return None

def extractRegExByGroup(regex, matchsting, groupname):
    r''' This function uses regex to match and extract required value data from the matchsting
        it uses group name, so make sure regex pattern include group name for the required pattern to extract, i.e:
        (?P<date>\d{1,2}\/\d{1,2}\/\d{2}) - match for dare pattern and names the match group 'date' '''
    extractedMatchString = None
    try:
        # Return an iterator yielding match objects over non-overlapping matches of pattern in string
        matches = re.finditer(regex, matchsting, re.MULTILINE)
        # loop over iterator to look if we have the group in one of the matchs
        for matchNum, match in enumerate(matches, start=1):
            # Check if we have the group in this match
            extractedMatchString = match.group(groupname)
            if extractedMatchString:
                # Found our group - exit the loop
                break
    except Exception as ex:
        print(ex)
    finally:
        return extractedMatchString