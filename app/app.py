from flask import Flask, redirect, render_template, request, url_for, flash, abort
from api import get_weather_by_city, get_weather_by_cities_in_circle


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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

    return render_template(f'weather/index.html')

@app.route('/<city_name>')
def result(city_name):
    res = get_weather_by_city(city=city_name)
    if res.ok:
        data = res.json()
        print("Response\n", data)
        return render_template('weather/result.html', data=data)
    else:
        print(res.json()['message'])
        abort(404, description=res.json()['message'])

@app.route('/test')
def test():
    res = get_weather_by_cities_in_circle()
    if res.ok:
        data = res.json()
        print("Response\n", res)
        return render_template('weather/test.html', data=data)
    else:
        print(res.json()['message'])
        abort(404, description=res.json()['message'])

if __name__ == '__main__':
    app.run(debug=True,)