from flask import Flask, redirect, render_template, request, url_for, flash, abort, send_from_directory, jsonify
from helper import get_icon_class
from owm_wrapper import OWM_API
import os


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
owm_api = OWM_API()

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
            return redirect(url_for("result", city_name=city))

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
    data = request.get_json()
    print("AJAX", data)
    return jsonify(data)

@app.route('/geo_test', methods=['GET', 'POST'])
def geo_loc():
    if request.method == "POST":
        data = request.get_json()
        print("AJAX", data)
    # return jsonify(data)
    return render_template('geo_test.html')

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
    if res.ok:
        data = res.json()
        print("Response\n", res)
        return render_template('weather/5_days_forecast.html', data=data)
    else:
        print(res.json()['message'])
        abort(404, description=res.json()['message'])
    
@app.route('/forecast-7-days')
def forecast_7_days():
    res = owm_api.get_7_days_forecast_by_coord()
    if res.ok:
        data = res.json()
        print("Response\n", res)
        return render_template('weather/5_day_forecast.html', data=data)
    else:
        print(res.json()['message'])
        abort(404, description=res.json()['message'])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True,)