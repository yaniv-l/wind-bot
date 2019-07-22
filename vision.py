from google.cloud import vision
from google.cloud.vision import types

from utils import extractRegExByGroup


def getDataFromImage(imageUrl):
    read = None
    client = vision.ImageAnnotatorClient.from_service_account_file('wind-info-b86a657f027d.json.secret')
    response = client.annotate_image({
    'image': {'source': {'image_uri': imageUrl}},
    'features': [{'type': vision.enums.Feature.Type.TEXT_DETECTION}],
    })
    texts = [text.description for text in response.text_annotations]
   
    if texts[0] is not None:
        data = texts[0]
        print(data)
        # create a dictioonary of the with read data of interest - value are extracted using regex
        read = {"readDate" : extractRegExByGroup(r"((?<=\\n)|(?<=^))(?P<date>\d{1,2}\/\d{1,2}\/\d{2})(?=\\n|\s|$)", data, 'date'),
                # (00|[0-1]{1}[0-9]{1}|2{1}[0-3]{1}):([0-5]{1}[0-9]{1}) # Correct time format
                "readTime" : extractRegExByGroup(r"((?<=\/\d{2}\s)|(?<=\\n))(?P<time>\d{1,2}:\d{2})(?=\\n|$)", data, 'time'),
                "wind": extractRegExByGroup(r"((?<=\\n)|(?<=^))(?P<wind>\d{1,3})(?=kts[\\n|$])", data, 'wind'),
                "gusts": extractRegExByGroup(r"(?<=Gust:\s)(?P<gust>.{1,3})(?=kts)", data, 'gust'),
                "dir": extractRegExByGroup(r"(?<=\()(?P<dir>\d{1,3}°?)(?=\)?)", data, 'dir'),
                "barometer": extractRegExByGroup(r"(?P<barometer>\d{3,4}.\d{1,2})(?=mb)", data, 'barometer')}
    return read

    


# data = "Freegull Sea Sports Sdot Yam Nautical Center\\nwww.wind.co.il\\nStation1 Surf Club \\\\ Shop Tel: 074-7012930\\n13:15\\n24/4/19\\nALMANAC\\nTEMP\\nWINDS\\nCURRENT\\nHumidity: 0%\\nDew Point: 0.0\\nWind Chl 0.0\\nBarometer 1021.31mb Moonset: 9:58\\nSunrise: 6:07\\n45-\\nHigh\\n0.0\\nLaw\\n0.0\\nRate\\n0.00%hr\\nSunset: 19:28\\n30\\n20\\n10\\n3-\\nMoonrise:-\\nRate: 0.894mb/hr Moon Day: 19\\nRain Today: 0.00mm\\nHourly: 0.00mm\\n3kts\\nS (184) Monthly: 420mm\\n0.0°\\nTotal:: 688.50mn\\n81%\\nGust: 4kts\\n"


    # (?<=P\<)[A-z]*(?=\>)  # Extract the group name from a regex, i.e (?<=\()(?P<test>\d{1,3}°?)(?=\)) > test
    #  gust (Gust: .{1,3}kts) # use . instead of \d since sometimes vision id number as charecter, like ekts instead of 6kts
    #       dir (\(\d{1,3}?°{0,1}\)) # (51°)
    #           wind (\\n\d{1,3}kts\\n) # \n5kts\n
    #               barometer (\d{3,4}.\d{1,2}mb) # 1021.95mb
    #                   datetime (\d{1,2}\/\d{1,2}\/\d{2})\\n\d{1,2}:\d{2} # 24/4/19\n12:32
    #       time \\n\d{1,2}:\d{2}\\n
    #        date (\\n\d{1,2}\/\d{1,2}\/\d{2}\\n)