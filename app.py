import requests
from bs4 import BeautifulSoup

# Function to extract data from html repsonse
def extract_data(response):
    data={}
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.select("h1",{"class": "header-desktop__AppName-xc5gow-5 fzCqyh"})
    data["name"]=name[0].text
    version = soup.find_all("div", {"class": "mini-versions__LatestVersion-sc-19sko2j-5 drfVqx"})
    data["version"]=version[0].text
    downloads = soup.find_all("span", {"class": "mini-stats__Info-sc-188veh1-6 hwoUxO"})
    data["downloads"]=downloads[0].text
    description = soup.find_all("p", {"class": "description__Paragraph-sc-45j1b1-1 daWyZe"})
    data["description"]=description[0].text
    release_date = soup.find_all("div", {"class": "mini-versions__VersionDate-sc-19sko2j-6 jeuKzx"})
    data['release_date']=release_date[0].text[1:-1]
    return data


response = requests.get("https://whatsapp.en.aptoide.com/app")
file1 = open('response.html', 'w', encoding="utf-8")
file1.write(str(response.text))
file1.close()
data=extract_data(response)
print("Name of the app: {app_name}".format(app_name=data.get('name')))
print("Version of the app: {app_version}".format(app_version=data.get('version')))
print("Number of downloads: {app_downloads}".format(app_downloads=data.get('downloads')))
print("App description: {app_description}".format(app_description=data.get('description')))
print("Release date: {app_release}".format(app_release=data.get('release_date')))
