import requests
from flask import *
from bs4 import BeautifulSoup

# Function to extract data from html repsonse
def extract_data(response):
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
    data['Release Date'] = release_date[0].text[1:-1]
    return data

app = Flask(__name__)
# random secret_key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    response = requests.get("https://whatsapp.en.aptoide.com/app")
    extracted_data = extract_data(response)
    return render_template('get-info.html',data=extracted_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)