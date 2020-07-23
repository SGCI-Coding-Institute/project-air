import csv
import os
# from collections import OrderedDict
# from csv import DictReader
# from typing import Dict, Union
from urllib.request import urlretrieve as retrieve
from werkzeug.utils import secure_filename
# from _collections import defaultdict

from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to connect our HTML file
# TODO: Expand on our base HTML page to provide more details about our project and add links to view our other /.. pages - Done
@app.route('/')
def index():
    return render_template('index.html')


# Function to get a COVID-19 data file and display the contents of it
# TODO: Make it so that we get this file from user url -Done
@app.route('/covid')
def import_covid_csv():
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    retrieve(url, 'covid_file/us.csv')

    with open('covid_file/us.csv', 'r') as covidfile:
        csv_read = csv.DictReader(covidfile)
        #print(csv_read)
        covid_list = []

        for i in csv_read:
            # print(i)
            date = i['date']
            cases = i['cases']
            deaths = i['deaths']
            # print(date, cases, deaths)
            covid_list.append({'date': date, 'cases': cases, 'deaths': deaths})
            # print(covid_list)

        return render_template('covid.html', l=covid_list)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload')
def upload_file():
    return render_template('data.html')


# Function to get a data file and display the contents of it
# TODO: Make it so that we get this file from user upload/input -Done
@app.route('/uploader', methods=['GET', 'POST'])
def get_second_csv():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template('data.html')


def compute_csv(covid, second_csv):
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
