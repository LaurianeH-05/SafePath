from flask import Flask, render_template, request, redirect, flash, url_for
import pandas as pd
from sodapy import Socrata
import sqlite3
from parse_incident import parse_incident_data
from datetime import datetime
from collections import defaultdict
from crime import get_crime_coordinates
import re
import googlemaps
from dotenv import load_dotenv
import os
from geopy.distance import geodesic

#Load environment variables from .env
load_dotenv()
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
crime_coordinates = get_crime_coordinates()

#Google Maps Functions
def clean_html(text):
    return re.sub('<[^<]+?>', '', text)

# Group crimes for formatting
def group_crimes_by_location(nearby_crimes):
    #Changed set to list
    grouped_crimes = defaultdict(list)
    for crime in nearby_crimes:
        lat, lon, location, incident_type,label, date = crime
        parts = crime[2].split("BLK")
        if len(parts) >= 2:
            block = parts[0].strip() + " BLK"
            street = parts[1].strip()
        else:
            block =location
            street = "Unknown"
        grouped_crimes[street].append({
            'block': block,
            'incident_type': f"{incident_type} - {label}",
            'date': date or "Unknown"
        })
    return grouped_crimes

#Check crimes nearby
def get_nearby_crimes(route, crime_coordinates, radius=161):  # About 0.1 miles
    route_coordinates = [
        (step['start_location']['lat'], step['start_location']['lng'])
        for step in route[0]['legs'][0]['steps']
    ]
    nearby_crimes = set()
    for route_point in route_coordinates:
        for crime_point in crime_coordinates:
            route_latlon = (route_point[0], route_point[1])
            crime_latlon = (crime_point[0], crime_point[1])
            if geodesic(route_latlon, crime_latlon).meters <= radius:
                nearby_crimes.add(crime_point)
    return nearby_crimes

# Function to get route from one location to another location
def get_route(start, end):
    # Request directions
    return gmaps.directions(start, end, mode="driving", alternatives=False, units="metric")




#Flask Application Setup and Routes
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
    results = client.get("icn6-v9z3", limit=2000)
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

@app.route('/route', methods=['GET','POST'])
def route_page():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        route = get_route(start, end)

        #Print route details
        steps = []
        for step in route[0]['legs'][0]['steps']:
            instruction = clean_html(step['html_instructions'])
            steps.append({
                'instruction': instruction,
                'distance': step['distance']['text'],
                'duration': step['duration']['text']
            })
        # Check for nearby crimes
        nearby_crimes = get_nearby_crimes(route, crime_coordinates)
        grouped = group_crimes_by_location(nearby_crimes)
        return render_template('route.html', steps=steps, nearby_crimes=grouped, start=start, end=end) 
    return render_template('route.html', steps=None, nearby_crimes=None, start=None, end=None)



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

    app.run(host="0.0.0.0", port=5000)
