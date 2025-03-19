# Import libraries
import os
import json
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from cachetools import TTLCache
# Declare a TTL Cache
weather_cache = TTLCache(maxsize=100, ttl=900)



# def check_city_in_country(city, country):
#     geolocator = Nominatim(user_agent="geo_checker")
#     location = geolocator.geocode(f"{city}, {country}")
#     if location:
#         if country.lower() in location.address.lower() and location.address.lower().startswith(city.lower()):
#             return True
#     return False

# # Check if a city exists given the city and country
# def check_valid_city(city: str) -> bool:
#     """Validate if a city exists in a given country."""
#     geolocator = Nominatim(user_agent="city_checker")
#     location = geolocator.geocode(city)
#     print(location)
#     if location and 'city' in location.raw['addresstype']:
#         return True
#     return False

# Get the weather of a city
def get_weather(city: str, country: str):
    if f"{city.lower()}_{country.lower()}" in weather_cache:
        return weather_cache[f"{city.lower()}_{country.lower()}"]
    base_url = "http://api.weatherstack.com/current"
    params = {
        'access_key': os.getenv('WEATHER_API_KEY'),
        'query': f"{city},{country}"
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        res = {}
        if response.status_code == 200 and 'current' in data:
            res['temperature'] = data['current']['temperature']
            res['wind_speed'] = data['current']['wind_speed']
            res['humidity'] = data['current']['humidity']
            res['feelslike'] = data['current']['feelslike']
            weather_cache[f"{city.lower()}_{country.lower()}"] = res
            return res
        else:
            return "Unable to fetch weather data!"
    except requests.RequestException as e:
        return "Weather service is down!"


