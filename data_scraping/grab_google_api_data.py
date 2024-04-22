import requests
import pandas as pd
import json
import time

def get_nearby_places_count(api_key, lat, lng, types):
    places_count = 0
    for place_type in types:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=1000&type={place_type}&key={api_key}"
        response = requests.get(url)
        data = response.json()
        if 'results' in data:
            places_count += len(data['results'])
            while 'next_page_token' in data:
                next_page_token = data['next_page_token']
                url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=1000&type={place_type}&key={api_key}&pagetoken={next_page_token}"
                response = requests.get(url)
                data = response.json()
                if 'results' in data:
                    places_count += len(data['results'])
    return places_count

def find_operational_places_and_average_price(api_key, lat, lng, radius=1000, place_type="restaurant"):
    operational_places = []
    price_levels = []
    
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": api_key,
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": place_type
    }
    
    while True:
        response = requests.get(url, params=params).json()
        results = response.get("results", [])
        
        for result in results:
            if result.get("business_status") == "OPERATIONAL":
                operational_places.append(result)
                # Extract the price level if it exists
                if "price_level" in result:
                    price_levels.append(result["price_level"])
        
        next_page_token = response.get("next_page_token")
        if not next_page_token:
            break
        
        time.sleep(2)
        params["pagetoken"] = next_page_token
    
    # Calculate the average price level if there are any price levels available
    average_price_level = sum(price_levels) / len(price_levels) if price_levels else None
    
    return len(operational_places), average_price_level

def get_address(api_key, lat, lng):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'results' in data and data['results']:
        return data['results'][0]['formatted_address']
    return None

def get_zip_code(address):
    if address is None:
        return None
    parts = address.split(',')
    if len(parts) >= 2:
        return parts[-2].strip()
    return None

def process_feature(api_key, feature):
    lng, lat = feature['geometry']['coordinates']
    address = get_address(api_key, lat, lng)
    if address is None:
        print(f"Address not found for coordinates: {lat}, {lng}")
        return None
    zip_code = get_zip_code(address)
    
    # For parks, we're only interested in the count, not the average price level
    parks_count, _ = find_operational_places_and_average_price(api_key, lat, lng, radius=1000, place_type="park")
    # For restaurants, we're interested in both count and average price level
    restaurants_count, average_price_level = find_operational_places_and_average_price(api_key, lat, lng)
    
    return {
        'Address': address,
        'Zip Code': zip_code,
        'Latitude': lat,
        'Longitude': lng,
        'Parks Count': parks_count,
        'Restaurants Count': restaurants_count,
        'Average Price Level': average_price_level  
    }

api_key = "api_key"
with open("centers(1).json", 'r') as f:
    data = json.load(f)

results = [process_feature(api_key, feature) for feature in data['features']]

df = pd.DataFrame([r for r in results if r is not None])
df.to_csv('places_count_with_address_4_2.csv', index=False)
