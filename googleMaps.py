#pip install googlemaps
import googlemaps
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

#Function to get route from one location to another
def get_route(start, end):
    #Request directions
    directions_result = gmaps.directions(start, end, mode="driving", alternatives=True, units="metric") 
    return directions_result

#User input for start and end locations
start = input("Enter the starting location: ")
end = input("Enter the destination location: ")
# Get the route
route = get_route(start, end)


# Print the route details
print("Route from {} to {}:".format(start, end))
for step in route[0]['legs'][0]['steps']:
    print(step['html_instructions'])
    print("Distance: {}".format(step['distance']['text']))
    print("Duration: {}".format(step['duration']['text']))
