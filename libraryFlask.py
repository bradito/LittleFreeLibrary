# libraryFlask.py
from flask import Flask, render_template
from astral import Astral
from littlefreelibrary import *
from time import sleep

import datetime
app = Flask(__name__)
print("starting serial connect attempt")
ser = Serial(port='/dev/ttyACM0', timeout=0)
sleep(2)
print("serial connected")
lib = LittleFreeLibrary(ser)
print("library object created")
# create library object

# need reconnection method here or in library
# need to be able to change program
# finalize method for main to catch program change and submit command and confirm the program changed.
# change main template to actually submit the program change


@app.route("/")
def hello():
	now = datetime.datetime.now()
	timestring = now.strftime("%Y-%m-%d %H:%M")

	if(not lib.lastCommandError):

		templateData = {
			'title':'Little Free Library',
			'time' : timestring,
			'programs': lib.programs,
			'currentProgram': lib.currentProgram
			}

		return render_template('main.html', **templateData)
	else:
		return render_template('notConnected.html')

@app.route('/update/<action>')
def update(action):
	"""
	set a new program from the letter in the URL
	"""

	lib.sendCommand(lib.prefix + action)
	now = datetime.datetime.now()
	timestring = now.strftime("%Y-%m-%d %H:%M")

	if(not lib.lastCommandError):

		templateData = {
			'title':'Little Free Library',
			'message': 'Update attempted!',
			'time' : timestring,
			'programs': lib.programs,
			'currentProgram': lib.currentProgram
			}

		return render_template('main.html', **templateData)
	else:
		return render_template('notConnected.html')


@app.route("/sunset")
def sunset():
	city_name = 'Minneapolis'
	a = Astral()
	a.solar_depression = 'civil'

	city = a[city_name]
	sun = city.sun(date=datetime.datetime.now(), local=True)

	return 'Sunset for {}: {}'.format(city_name, sun['sunset'])


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=False)



