from datetime import datetime, timezone


class WeatherMoment:

    def __init__(self):
        pass
    
    @staticmethod
    def parse_current_day(current_weather):
        # Time of the weather data received
        timestamp = current_weather['dt']
        # Convert to local datetime
        local_datetime = datetime.fromtimestamp(timestamp)
        # Get date
        date = local_datetime.strftime('%B %-d, %Y')
        # Get day name of the week
        day_of_week = local_datetime.strftime('%A')
        # Temperature is measured in Celcius
        temperature = round(current_weather['temp'],0)
        # Weather condition
        description = current_weather['weather'][0]['description']
        icon_id = get_icon_class(current_weather['weather'][0]['id'])

        parsed_data = {}
        for variable in ["date", "day_of_week", "temperature", "description", "icon_id"]:
            parsed_data[variable] = eval(variable)
        return parsed_data

    @staticmethod
    def parse_daily_day(daily_weather):
        # Time of the weather data received
        timestamp = daily_weather['dt']
        # Convert to local datetime
        local_datetime = datetime.fromtimestamp(timestamp)
        # Get date
        date = local_datetime.strftime('%B %-d, %Y')
        # Get day name of the week
        day_of_week = local_datetime.strftime('%A')
        # Temperature is measured in Celcius
        temperature = int(round(daily_weather['temp']['day'],0))
        temp_min = int(round(daily_weather['temp']['min'],0))
        temp_max = int(round(daily_weather['temp']['max'],0))
        # Weather condition
        description = daily_weather['weather'][0]['description']
        icon_id = get_icon_class(daily_weather['weather'][0]['id'])

        parsed_data = {}
        for variable in ["date", "day_of_week", "temperature", "description", "icon_id", "temp_max", "temp_min"]:
            parsed_data[variable] = eval(variable)
        return parsed_data

# TODO: define day and night -> wi-owm-day-<code> / wi-owm-night-<code>
def get_icon_class(icon_id):
    return f"wi-owm-{icon_id}"
    