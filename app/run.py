from flask import Flask, redirect, render_template, request, url_for, flash
from api import get_weather_by_city


app = Flask(__name__)

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
    data = get_weather_by_city(city=city_name)
    if data:
        print("Response\n", data)
    return render_template('weather/result.html', city_name=city_name, data=data)

def redirect_url(default='weather/index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

if __name__ == '__main__':
    app.run(debug=True,)