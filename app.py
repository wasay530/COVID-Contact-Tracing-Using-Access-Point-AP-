from flask import Flask, url_for, render_template, flash, request, redirect, session,logging,request
from flask_sqlalchemy import SQLAlchemy
import requests
import json

import time
from datetime import datetime

from beacontools import BeaconScanner, IBeaconFilter, IBeaconAdvertisement
from csv import writer
from csv import DictWriter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# IP address to test (your global ip address)
ip_address = '203.253.145.194'

# URL to send the request to
request_url = 'https://geolocation-db.com/jsonp/' + ip_address
# Send request and decode the result
response = requests.get(request_url)
result = response.content.decode()
# Clean the returned string so it just contains the dictionary data for the IP address
result = result.split("(")[1].strip(")")
# Convert this data into a dictionary
result  = json.loads(result)
latitude = result['latitude']
long = result['longitude']

c = 10.0
i = 0

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:

        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def callback(bt_addr, rssi, packet, additional_info):
    #uuidd = int(uuidd)
    y = (-69-(rssi))/(20)
    distance = c ** y
    now = datetime.now()
    curr_time = now.strftime("%H:%M:%S")
    curr_date = now.strftime("%D")
    print("Beacon Scanning")
    row_contents = [curr_date,curr_time,additional_info['uuid'],distance]    
   # print('*** Append new row to an existing csv file using csv.writer() in python ***')
        # Append a list as new line to an old csv file
    append_list_as_row('Beacons.csv', row_contents)
    print("%s %s %f %s" % (curr_date, curr_time, distance, additional_info['uuid']))

scanner = BeaconScanner(callback,packet_filter=IBeaconAdvertisement)
if i == 0:
    i = 1
    row_contents = ["date","time","beaconid_others","distance"]

scanner.start()

class User(db.Model):
	""" Create user table"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))

	def __init__(self, username, password):
		self.username = username
		self.password = password


@app.route('/', methods=['GET', 'POST'])
def home():
	""" Session control"""
	if not session.get('logged_in'):
		return render_template('index.html')
	else:
		if request.method == 'POST':

			return render_template('index.html') 
		return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Login Form"""
	if request.method == 'GET':
		return render_template('login.html')
	else:
		name = request.form['username']
		passw = request.form['password']
		try:
			data = User.query.filter_by(username=name, password=passw).first()
			if data is not None:
				session['logged_in'] = True
				return redirect(url_for('home'))
			else:
				return 'Incorrect Login'
		except:
			return "Incorrect Login"

@app.route('/register/', methods=['GET', 'POST'])
def register():
	"""Register Form"""
	if request.method == 'POST':
		new_user = User(username=request.form['username'], password=request.form['password'])
		db.session.add(new_user)
		db.session.commit()
		return render_template('login.html')
	return render_template('register.html')

@app.route("/logout")
def logout():
	"""Logout Form"""
	session['logged_in'] = False
	return redirect(url_for('home'))


if __name__ == '__main__':
	app.debug = True
	db.create_all()
	app.secret_key = "123"
	app.run(host='0.0.0.0')
	
