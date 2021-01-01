import os
import requests

API_KEY = os.environ.get("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/"

def get_weather_by_city(city='London'):
    try:
        res = requests.get(url=BASE_URL+"weather", params=dict(q=city, units="metric", APPID=API_KEY))
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

def get_weather_by_cities_in_circle():
    try:
        res = requests.get(url=BASE_URL+"find", params=dict(lat=55, lon=37.5, cnt=10, APPID=API_KEY))
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