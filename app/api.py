import os
import requests

API_KEY = os.environ.get("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_by_city(city='London'):
    try:
        res = requests.get(url=BASE_URL, params=dict(q=city, units="metric", APPID=API_KEY))
        res.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    finally:
        return res