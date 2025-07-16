import json

def parse_incident_data(json_data):
    """
    Parse incident JSON data and extract incident ID and location information
    """
    # Parse the JSON string if it's a string, otherwise use as is
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    # Extract incident ID
    incident_id = data.get('incident_id')
    
    # Extract location information
    location_info = {
        'incident_id': incident_id,
        'address': f"{data.get('address_number', '')} {data.get('address_street', '')} {data.get('street_type', '')}",
        'city': data.get('city'),
        'state': data.get('state'),
        'zip_code': data.get('zip_code'),
        'location': data.get('location'),
        'latitude': data.get('latitude'),
        'longitude': data.get('longitude'),
        'district': data.get('district'),
        'place': data.get('place')
    }
    
    return location_info

def display_crime_locations(data):
    """
    Accepts a DataFrame or list of dicts, parses each record, and prints location info for each crime.
    """
    from pandas import DataFrame
    if isinstance(data, DataFrame):
        records = data.to_dict(orient='records')
    else:
        records = data
    
    for i, record in enumerate(records, 1):
        info = parse_incident_data(record)
        print(f"Crime #{i}:")
        print(f"  Location: {info.get('location', '')}")
        print(f"  City: {info.get('city', '')}")
        print(f"  State: {info.get('state', '')}")
        print(f"  ZIP Code: {info.get('zip_code', '')}")
        print(f"  Latitude: {info.get('latitude', '')}")
        print(f"  Longitude: {info.get('longitude', '')}")
        print('-' * 40)

# Sample data
sample_data = {
    "incident_id": "201536320",
    "offence_code": "9042",
    "case_number": "250031423",
    "date": "2025-07-14T17:42:01.000",
    "start_date": "2025-07-14T17:42:00.000",
    "nibrs_code": "90Z",
    "victims": "1",
    "crimename1": "Crime Against Society",
    "crimename2": "All Other Offenses",
    "crimename3": "SUICIDE - ATTEMPT",
    "district": "BETHESDA",
    "location": "4100 BLK  KNOWLES AVE",
    "city": "KENSINGTON",
    "state": "MD",
    "zip_code": "20895",
    "agency": "MCPD",
    "place": "Residence - Single Family",
    "sector": "D",
    "beat": "2D1",
    "pra": "182",
    "address_number": "4100",
    "address_street": "KNOWLES",
    "street_type": "AVE",
    "latitude": "39.02779",
    "longitude": "-77.0795",
    "police_district_number": "2D",
    "geolocation": {
        "latitude": "39.0278",
        "longitude": "-77.0795",
        "human_address": "{\"address\": \"\", \"city\": \"\", \"state\": \"\", \"zip\": \"\"}"
    },
    ":@computed_region_vu5j_pcmz": "1",
    ":@computed_region_tx5f_5em3": "1",
    ":@computed_region_kbsp_ykn9": "15",
    ":@computed_region_d7bw_bq6x": "25",
    ":@computed_region_rbt8_3x7n": "1",
    ":@computed_region_a9cs_3ed7": "1",
    ":@computed_region_r648_kzwt": "4",
    ":@computed_region_d9ke_fpxt": "1",
    ":@computed_region_6vgr_duib": "7"
}

if __name__ == "__main__":
    # Parse the sample data
    result = parse_incident_data(sample_data)
    
    print("Parsed Incident Data:")
    print(f"Incident ID: {result['incident_id']}")
    print(f"Full Address: {result['address']}")
    print(f"City: {result['city']}")
    print(f"State: {result['state']}")
    print(f"ZIP Code: {result['zip_code']}")
    print(f"Location: {result['location']}")
    print(f"Latitude: {result['latitude']}")
    print(f"Longitude: {result['longitude']}")
    print(f"District: {result['district']}")
    print(f"Place Type: {result['place']}")
    
    # You can also access the coordinates for mapping
    print(f"\nCoordinates: {result['latitude']}, {result['longitude']}") 