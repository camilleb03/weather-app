import datetime as dt

# TODO: define day and night -> wi-owm-day-<code> / wi-owm-night-<code>
def get_icon_class(data):
    weather_id = data['weather'][0]['id']
    print("WEATHER_ID", data['weather'][0]['id'])
    return f"wi-owm-{weather_id}"

