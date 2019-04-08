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
    
    url = "http://www.surfo.co.il/%D7%9E%D7%96%D7%92-%D7%90%D7%95%D7%95%D7%99%D7%A8"
    response = simple_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        info = windInfo("surfo", url, WindSpdUnit.KN)
        scrapWebData(html, info)
    else:   
        # Raise an exception if we failed to get any data from the url
        raise Exception('Error retrieving contents at {}'.format(url))


def scrapWebData(html, info):
    div = html.find("div", attrs={"class" : "w_line firstline"})
    info.readDateTime = str(div.contents[0].contents[0])
    info.Temp = str(div.contents[5].contents[0])
    info.windAvg = str(div.contents[2].contents[0])
    info.windGust = str(div.contents[3].contents[0])
    info.windDir = str(div.contents[1].contents[0])
    updatedate = html.find("span", attrs={"id": "ContentPlaceHolder1_date"})
    info.infoDate = updatedate.contents[0]
    pass

getWinds()