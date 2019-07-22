from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from windInfo import windInfo, WindSpdUnit

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

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True, verify=False, headers={'Cache-Control': 'no-cache'})) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def getWinds():
    """
    Downloads the page where the list of mathematicians is found
    and returns a list of strings, one per mathematician
    """
    
    url = "https://www.hobolink.com/p/bb5b1433de5f0ebae4d54a44123c7e4b"
    response = simple_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        info = windInfo("Dor-Nachsholim", url, WindSpdUnit.KN)
        scrapWebData(html, info)
    else:   
        # Raise an exception if we failed to get any data from the url
        raise Exception('Error retrieving contents at {}'.format(url))


def scrapWebData(html, info):
    info.readDateTime = html.find("span", attrs={"id" : "latestConditionsQtip"}).contents[0]
    tbody = html.find("tbody", attrs={"id" : "hobolink-latest-conditions-form:conditions-tree_data"})
    info.Temp = str(tbody.contents[1].contents[0].contents[10].contents[1].contents[1].contents[0].contents[0])
    info.windAvg = str(tbody.contents[4].contents[0].contents[10].contents[1].contents[1].contents[0].contents[0])
    info.windGust = str(tbody.contents[6].contents[0].contents[10].contents[1].contents[1].contents[0].contents[0])
    info.windDir = str(tbody.contents[5].contents[0].contents[10].contents[1].contents[1].contents[0])
    info.barometerPreasure = str(tbody.contents[9].contents[0].contents[10].contents[1].contents[1].contents[0].contents[0])
    pass

getWinds()