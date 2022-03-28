import requests
from flask import Flask,redirect,flash,request,render_template
from bs4 import BeautifulSoup
import re
from typing import Union,Optional
import mypy
from requests_html import HTMLSession

[mypy]
ignore_missing_imports = True

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
            return url

    return None

# Function to extract data from html repsonse
def extract_data(response:requests.Response)->dict:
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

# checks if input contains valid aptoid url using regex
def match(input)->bool:
    if (re.search("[a-zA-Z0-9]+\\.en\\.aptoide\\.com/app",input)):
        return True
    else:
        return False

app = Flask(__name__)
# random secret_key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-info',methods=['post'])
def get_info(query_url:str="")-> Union[str,requests.Response]:
    url = query_url if query_url != "" else request.form.get('url')
    if (match(url) == False):
        flash("Please provide a correct aptoide URL")
        return redirect("/")
    elif (url!=""):
        response = requests.get(url)
        extracted_data = extract_data(response)
        return render_template('get-info.html',data=extracted_data)
    else:
        return redirect("/")

@app.route('/get-info-by-name',methods=['post'])
def get_info_by_name()-> requests.Response:
    search_name = request.form.get('name')
    search_result = find_link(search_name) if search_name!="" else None
    if (search_result != None):
        return get_info(search_result)
    else:
        if(search_name!=""):
            flash("Oups! Could not find the app by name, try searching using an Aptoide URL")
        else:
            flash("You should provide an app name to use this feature")
        return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)   