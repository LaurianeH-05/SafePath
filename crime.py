# API_KEY = 928lk5zsav6givzzkh69lzt3j
# API_SECRET = 514ld6hw1x45ikk2e55hsbkak44asws48nmzmvurxdqmlo0u8u

#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
from parse_incident import parse_incident_data, display_crime_locations

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.montgomerycountymd.gov", "5bwthyARYMArZxzjQH51yZQzQ")

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.montgomerycountymd.gov,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
def get_crime_coordinates():
    results = client.get("icn6-v9z3", limit=2000)
    crime_coordinates = []
    for result in results:
        lat = float(result.get('latitude'))
        lon = float(result.get('longitude'))
        location = result.get('location')
        if lat and lon and location:
            crime_coordinates.append((lat, lon, location))
    return crime_coordinates
# Convert to pandas DataFrame
# results_df = pd.DataFrame.from_records(results)
# display_crime_locations(results_df)
# print(parse_incident_data(results_df))
#print(results_df)