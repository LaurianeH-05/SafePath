from flask import Flask, render_template, request, redirect, flash, url_for
import pandas as pd
from sodapy import Socrata
import sqlite3
from parse_incident import parse_incident_data
from datetime import datetime

app = Flask(__name__)
#add secret_key here!

@app.route('/')
def home():
    return render_template('home.html')

#route to safety tips page
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

#route to show the form
@app.route('/report')
def report():
    return render_template('report.html')

#route to process the form
@app.route('/submit_report', methods=['POST'])
def submit_report():
    location = request.form['location']
    report_type = request.form['type']
    description = request.form['description']

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO reports (location, type, description, timestamp) VALUES (?, ?, ?, ?)",
              (location, report_type, description, datetime.now()))
    conn.commit()
    conn.close()

    flash('Thank you for your report')
    return redirect(url_for('report'))

if __name__ == '__main__':
    import sqlite3

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS reports (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              location TEXT NOT NULL,
              type TEXT NOT NULL,
              description TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP) 
              """);
    conn.commit()
    conn.close()

    app.run(debug=True)
