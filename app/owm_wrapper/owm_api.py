import os
import requests

class OWM_API:
    def __init__(self):

        self.OWM_API_KEY = os.environ.get("OWM_API_KEY", None)
        self.OWM_BASE_URL = "http://api.openweathermap.org/data/2.5/"

    def get_current_weather_by_city_name(self, city, units="metric"):
        try:
            res = requests.get(url=self.OWM_BASE_URL+"weather", params=dict(q=city, units=units, APPID=self.OWM_API_KEY))
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

    def get_current_weather_by_coord_in_circle(self, lat=55, lon=37.5, cnt=10):
        try:
            res = requests.get(url=self.OWM_BASE_URL+"find", params=dict(lat=lat, lon=lon, cnt=cnt, APPID=self.OWM_API_KEY))
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

    def get_5_days_forecast_by_city_name(self, city):
        try:
            res = requests.get(url=self.OWM_BASE_URL+"forecast", params=dict(q=city, APPID=self.OWM_API_KEY))
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

    def get_7_days_forecast_by_coord(self, lat=55, lon=37.5, exclude="current,minutely,hourly,alerts"):
        try:
            res = requests.get(url=self.OWM_BASE_URL+"onecall", params=dict(lat=lat, lon=lon, exclude=exclude, APPID=self.OWM_API_KEY))
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

    @staticmethod
    def get_user_location(ip_address):
        try:
            res = requests.get(f"http://ip-api.com/json/{ip_address}", params=dict(fields="status,message,lat,lon"))
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
        