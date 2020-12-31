import os
import requests

API_KEY = os.environ.get("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_by_city(city='London'):
    try:
        r = requests.get(url=BASE_URL, params=dict(q=city, APPID=API_KEY))
        return r.json()
    except Exception as e:
        print(e)
        return None