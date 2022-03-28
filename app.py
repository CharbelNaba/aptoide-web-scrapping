import requests
from flask import Flask, redirect, flash, request, render_template
from typing import Union
from utils import extract_data, match, find_link
import werkzeug

app = Flask(__name__)
# random secret_key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index()->str:
    return render_template('index.html')

@app.route('/get-info',methods=['post'])
def get_info(query_url:str="")-> Union[str,werkzeug.wrappers.response.Response]:
    url = query_url if query_url != "" else request.form.get('url')
    if (match(url) == False):
        flash("Please provide a correct aptoide URL")
        return redirect("/")
    elif (url!=""):
        response = requests.get(str(url))
        extracted_data = extract_data(response)
        return render_template('get-info.html',data=extracted_data)
    else:
        return redirect("/")

@app.route('/get-info-by-name',methods=['post'])
def get_info_by_name()-> werkzeug.wrappers.response.Response:
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