from typing import Optional,Union
import re
from requests_html import HTMLSession  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import requests

#The following app could have been done whith less line of code using the googlesearch module (public api)
def find_link(app_name:Optional[str])->Union[str,None]:
    session = HTMLSession()
    query = "{name}.en.aptoide.com/app".format(name=str(app_name).lower())
    response = session.get("https://www.google.com/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://translate.google.com/')
    
    for url in links[:]:
        if ((url.startswith(google_domains)==False and url.endswith(".en.aptoide.com/app")) and (query in url) and (re.search("[a-zA-Z0-9]+\\.en\\.aptoide\\.com/app",url))):
            session.close()
            return url
    session.close()
    return None

# Function to extract data from html repsonse
def extract_data(response:requests.Response)->Optional[dict]:
    try:
        data = {}
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.select("h1",{"class": "header-touch__AppName-sc-1om5ik5-5 PLRmn"})
        data["Name"] = name[0].text
        version = soup.find_all("div", {"class": "mini-versions__LatestVersion-sc-19sko2j-5 drfVqx"})
        data["Version"] = version[0].text
        downloads = soup.find_all("span", {"class": "mini-stats__Info-sc-188veh1-6 hwoUxO"})
        data["Downloads"] = downloads[0].text
        description = soup.find_all("p", {"class": "description__Paragraph-sc-45j1b1-1 daWyZe"})
        data["Description"] = description[0].text
        release_date = soup.find_all("div", {"class": "mini-versions__VersionDate-sc-19sko2j-6 jeuKzx"})
        data["Release Date"] = release_date[0].text[1:-1]
        return data
    except Exception:
        print("Could not gather the data")
        return None

# checks if input contains valid aptoid url using regex
def match(input)->bool:
    if (re.search("[a-zA-Z0-9]+\\.en\\.aptoide\\.com/app",input)):
        return True
    else:
        return False