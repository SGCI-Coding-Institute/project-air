from flask import Flask, render_template
from csv import DictReader

app = Flask(__name__)


# Function to connect our HTML file
# TODO: Expand on our base HTML page to provide more details about our project and add links to view our other /.. pages
@app.route('/')
def index():
    return render_template('index.html')


# Function to get a COVID-19 data file and display the contents of it
# TODO: Make it so that we get this file from user upload/input
@app.route('/covid')
def import_covid_csv():
    with open('/Users/hectorsantiago/Desktop/covid_data.csv', 'r') as covidfile:
        csv_read = DictReader(covidfile)

        for row in csv_read:
            return str(row)


# Function to get a Flu data file and display the contents of it
# TODO: Make it so that we get this file from user upload/input
@app.route('/flu')
def import_second_csv():
    # Opening our test Flu file in a read status
    file = open('/Users/hectorsantiago/Downloads/NCHS_-_Leading_Causes_of_Death__United_States.csv', 'r')
    with file:
        reader = DictReader(file)
        # Getting data only from the year 2017
        rows = [row for row in reader if row['\ufeffYear'] == '2017' and row['State'] == 'United States']

        return str(rows)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
