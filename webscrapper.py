from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json
from types import SimpleNamespace as Namespace

import consts
from windInfo import windInfo, WindSpdUnit
import firedata
import wind_tracker
from utils import config


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True, verify=False)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def getWinds():
    """
    Downloads the page where the list of mathematicians is found
    and returns a list of strings, one per mathematician
    """
    for source in [consts.SOURCEREAD.PRIGAL, consts.SOURCEREAD.EILAT_METEO_TECH]:
        url = config.get(source, "readsURL")
        windUnits = config.get(source, "windUnits")
        response = simple_get(url)
        if response is not None:
            html = BeautifulSoup(response, 'html.parser')
            info = windInfo(source, url, windUnits)
            scrapWebData(html, info)
            jsonInfo = info.toJSON()
            firedata.writeWindReads(jsonInfo)
            res = firedata.readWindReads(source)
            wind_tracker.sense_for_wind_change(res)
        else:   
            # Raise an exception if we failed to get any data from the url
            raise Exception('Error retrieving contents at {}'.format(url))


def scrapWebData(html, info):
    if info.infoSourceName == consts.SOURCEREAD.PRIGAL:
        info.windDir = html.find("div", attrs={"class" : "inf-wind-direction"}).contents[0].text
        info._infoDate = html.find("h3", attrs={"class" : "inf-time-date rel-gradient english"}).text
        info._infoTime = html.find("p", attrs={"class" : "inf-time-time english"}).text
        info.windStrength = html.find("div", attrs={"class" : "inf-wind-strength"}).contents[0].text
    elif info.infoSourceName == consts.SOURCEREAD.EILAT_METEO_TECH:
        tr = html.find("tr", attrs={"bgcolor" : "#ccffff"})
        info.windDir = str(tr.contents[7].contents[0].contents[0])
        info.readDateTime = str(tr.contents[1].contents[0].contents[0].contents[0])
        info.windAvg = tr.contents[8].contents[0].contents[0]
        info.windGust = tr.contents[9].contents[0].contents[0]
        info.waterTemp = tr.contents[11].contents[0].contents[0]
        info.barometerPreasure = tr.contents[5].contents[0].contents[0]
    else:
        pass


if __name__ == '__main__':
    print('Starting scrapping for wind reads....')
    getWinds()
    print('... done.\n')