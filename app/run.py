from flask import Flask, redirect, render_template, request, url_for, flash, abort, send_from_directory, jsonify
from helper import get_icon_class, parse_5_days_forecast, parse_current_and_daily_forecast
from owm_wrapper import OWM_API
import os
import json


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
owm_api = OWM_API()
user_location = None

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error/404.html', error=e), 404

@app.route('/', methods=("GET", "POST"))
def search():
    if request.method == "POST":
        city = request.form["city"]
        error = None

        if not city:
            error = "City is required."

        if error is not None:
            flash(error)
        else:
            return redirect(url_for("forecast_7_days", city_name=city))

    return render_template('weather/index.html')

@app.route('/<city_name>')
def result(city_name):
    res = owm_api.get_current_weather_by_city_name(city=city_name)
    if res.ok:
        data = res.json()
        icon_class = get_icon_class(data)
        print("ICON_CLASS:", icon_class)
        print("Response\n", data)
        return render_template('weather/result.html', data=data, icon_class=icon_class)
    else:
        print(res.json()['message'])
        abort(404, description=res.json()['message'])

@app.route('/postmethod', methods=['POST'])
def postmethod():
    user_location = request.get_json()
    print("LOC: ", user_location)
    return jsonify(user_location)

@app.route('/geo_test', methods=['GET', 'POST'])
def geo_test():
    if request.method == "POST":
        user_location = request.get_json()
        print("UL: ", user_location)
        return jsonify(user_location)
    if request.method == "GET":
        return render_template('geo_test.html', user_location=user_location)

@app.route('/geo_loc')
def geo_loc():
    ip_address = request.remote_addr
    print("IP: ", ip_address)
    res = owm_api.get_user_location(ip_address=ip_address)
    if res.ok and res.json()['status'] == 'success':
        data = res.json()
        print("Response\n", res)
        return render_template('weather/test.html', data=data)
    else:
        abort(404, description=res.json()['message'])

@app.route('/test')
def test():
    res = owm_api.get_current_weather_by_coord_in_circle()
    if res.ok:
        data = res.json()
        print("Response\n", res)
        return render_template('weather/test.html', data=data)
    else:
        print(res.json()['message'])
        abort(404, description=res.json()['message'])
    
@app.route('/forecast-5-days/<city_name>')
def forecast_5_day(city_name):
    res = owm_api.get_5_days_forecast_by_city_name(city_name)
    pretty_res = json.dumps(res.json(), sort_keys = True, indent = 4, separators = (',', ': '))
    if res.ok:
        data = res.json()
        parse_5_days_forecast(data)
        # print("Response\n", data)
        return render_template('weather/5_days_forecast.html', data=data)
    else:
        print(res.json()['message'])
        abort(404, description=res.json()['message'])
    
@app.route('/forecast-7-days/<city_name>')
def forecast_7_days(city_name):
    r = owm_api.get_city(city_name)
    if r.ok:
        if not r.json():
            abort(404, description="City not found")
        city_info = r.json()[0]
        country_name = city_info['address']['country']
        pretty_city = json.dumps(r.json(), sort_keys = True, indent = 4, separators = (',', ': '))
        
        res = owm_api.get_7_days_forecast_by_coord(lat=city_info['lat'], lon=city_info['lon'])
        retty_res = json.dumps(res.json(), sort_keys = True, indent = 4, separators = (',', ': '))
        print(res.url)
        if res.ok:
            data = res.json()
            current_weather, daily_weather = parse_current_and_daily_forecast(data)
            current_weather['country_name'] = country_name
            current_weather['city_name'] = city_name
            return render_template('weather/7_days_forecast.html', current_weather=current_weather, daily_weather=daily_weather)
        else:
            print(res.json()['message'])
            abort(404, description=res.json()['message'])
    else:
        print(res.json()['message'])
        abort(404, description=r.json()['message'])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)