from flask import Flask, render_template, url_for, request, redirect
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
	error = request.args.get('error')
	return render_template('weather.html', weather=None, error=error)

@app.route('/weather')
def weather():
	city = request.args.get('city')
	state = request.args.get('state')
	country = request.args.get('country')
	unit = request.args.get('unit')
	if state:
		req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&units={unit}&appid=a91de6f82cc3a3eab53bef9074ae4a70').json()
	else:
		req = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&units={unit}&APPID=a91de6f82cc3a3eab53bef9074ae4a70').json()
	weather = req['weather'][0]
	temp = req['main']
	return render_template('weather.html', weather=weather, temp=temp, unit=unit, city=city, state=state, country=country)

@app.route('/get_weather', methods=['POST'])
def get_weather():
	try:
		city = request.form['city']
		state = request.form['state'] if request.form['state'] != "" else None
		country = request.form['country']
		unit = request.form['unit-type']
		if city is "" or country is "":
			return redirect(url_for('index', error="Try again. You need a city and a country"))
		else:
			return redirect(url_for('weather', city=city, country=country, state=state, unit=unit))
	except:
		return redirect(url_for('index'))

port = int(os.environ.get("POST", 5010))
if __name__ == '__main__':
	app.run(threaded=True, port=port)
