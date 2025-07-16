from flask import Flask, render_template
import pandas as pd
from sodapy import Socrata
from parse_incident import parse_incident_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/crimes')
def crimes():
    client = Socrata("data.montgomerycountymd.gov", "5bwthyARYMArZxzjQH51yZQzQ")
    results = client.get("icn6-v9z3", limit=10)
    results_df = pd.DataFrame.from_records(results)
    parsed = results_df.apply(lambda row: parse_incident_data(row.to_dict()), axis=1)
    crimes_list = parsed.tolist()
    return render_template('crimes.html', crimes=crimes_list)

@app.route('/report')
def report():
    return render_template('report.html')
if __name__ == "__main__":
    app.run(debug=True)