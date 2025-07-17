#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
from parse_incident import parse_incident_data, display_crime_locations

client = Socrata("data.montgomerycountymd.gov", "5bwthyARYMArZxzjQH51yZQzQ")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
crime_code_map = {
    "2303": "Theft from Auto",
    "2304": "Vehicle Parts Theft",
    "2307": "Auto Theft",
    "2308": "Larceny from Building",
    "2399": "Larceny - Other",
    "2404": "Vehicle Theft",
    "2202": "Burglary - Forced Entry (Residence)",
    "5707": "Vehicle Burglary",
    "1202": "Burglary",
    "1399": "Assault (Other)",
    "2903": "Destruction of Property",
    "3504": "Drug Violation",
    "3550": "Alcohol Violation",
    "3572": "DUI",
    "5212": "Weapons Violation",
    "9021": "Disorderly Conduct",
    "9113": "Suspicious Situation",
    "9010": "Public Intoxication",
    "5704": "Attempted Vehicle Theft",
    "3102": "Forgery",
    "1801": "Fraud - General",
}
def get_crime_coordinates():
    results = client.get("icn6-v9z3", limit=2000)
    crime_coordinates = []
    for result in results:
        lat = float(result.get('latitude'))
        lon = float(result.get('longitude'))
        location = result.get('location')
        incident_type = result.get('offence_code')
        label = crime_code_map.get(incident_type, "Unknown")

        date = result.get('date').replace('T', ' ').split(".")[0] if result.get('date') else None
        if lat and lon and location and incident_type and date:
            crime_coordinates.append((lat, lon, location, incident_type, label, date))
    return crime_coordinates