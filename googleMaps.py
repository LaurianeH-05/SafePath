from collections import defaultdict
from crime import get_crime_coordinates
crime_coordinates = get_crime_coordinates()
import re
import googlemaps
from dotenv import load_dotenv
import os
from geopy.distance import geodesic
# Load environment variables from .env file
load_dotenv()
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

def clean_html(text):
    return re.sub('<[^<]+?>', '', text)
#Group crimes for formatting
def group_crimes_by_location(nearby_crimes):
    grouped_crimes = defaultdict(set)
    for crime in nearby_crimes:
        parts = crime[2].split("BLK")
        if len(parts) >= 2:
            block = parts[0].strip() + " BLK"
            street = parts[1].strip()
            grouped_crimes[street].add(block)
    return grouped_crimes

#Check nearby crimes
def get_nearby_crimes(route, crime_coordinates, radius=161): # About 0.1 miles
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


#Function to get route from one location to another
def get_route(start, end):
    #Request directions
    return gmaps.directions(start, end, mode="driving", alternatives=False, units="metric") 

#User input for start and end locations
start = input("Enter the starting location: ")
end = input("Enter the destination location: ")
# Get the route
route = get_route(start, end)


# Print the route details
print("Route from {} to {}:".format(start, end))
for step in route[0]['legs'][0]['steps']:
    instruction =clean_html(step['html_instructions'])
    print("-> {}".format(instruction))
    print("Distance: {} | Duration: {}\n".format(step['distance']['text'], step['duration']['text']))


# Check for nearby crimes
nearby_crimes = get_nearby_crimes(route, crime_coordinates)
if not nearby_crimes:
    print("No nearby crimes found.")
else:
    summary = group_crimes_by_location(nearby_crimes)
    print(f"\n{len(nearby_crimes)} nearby crimes detected.\n")
    for street, blocks in summary.items():
        print(f"Street: {street}")
        for block in sorted(blocks):
            print(f"\tAt {block}")