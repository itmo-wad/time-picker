""" Views file """

import os
import json
import base64
import requests
import mongodb_query
from app import app, mongo
from flask import Flask, send_from_directory, request, flash, redirect, render_template, session, url_for, jsonify




maps_URL = "https://geocode.search.hereapi.com/v1/geocode"
maps_api_key = app.config["MAPS_API"]
PARAMS = {'apikey':maps_api_key,'q':"Невский проспект"}#default address
latitude = 59.9138
longitude = 30.3483


#redirects to mainpage if logged in
#else - login
@app.route('/', methods = ['GET','POST'])
def login():
	if request.method == "POST":
		if mongodb_query.user_exist(request.form['username'], request.form['password']):
			session['username'] = request.form['username']
			return redirect('mainpage')
		else:
			flash("Wrong login or password!")
			return render_template('login_page.html')
	elif request.method == "GET":
		if 'username' in session:
			return redirect(url_for("mainpage"))
	return render_template('login_page.html')


#main page
@app.route('/mainpage')
def mainpage():
	if request.method == "GET":
		if 'username' in session:
			userdata = mongodb_query.showUser_info(session['username'])
			name = userdata[0]["surname"]+" "+userdata[0]["name"]
			try:
				avatar =  mongo.db.users_table.find_one({'username':session['username']})['avatar']
				return render_template('main_info.html', name = name, image=avatar, phone_num = userdata[0]["phone_number"])
			except KeyError:
				return render_template('main_info.html', name = name, phone_num = userdata[0]["phone_number"])
		else:
			return redirect ('/')


#it used just for testing to see each registered user
@app.route('/showregistered', methods = ['GET','POST'])
def showregistered():
	if 'username' in session:
		userdata = mongodb_query.showUser_info(session['username'])
		try:
			avatar =  mongo.db.users_table.find_one({'username':session['username']})['avatar']
			return render_template("setting_page.html", login = userdata[0]["login"], name = userdata[0]["name"], surname = userdata[0]["surname"], phone_num = userdata[0]["phone_number"], image=avatar, users = mongodb_query.showAllusers_table())
		except KeyError:
			return render_template("setting_page.html", login = userdata[0]["username"], name = userdata[0]["name"], surname = userdata[0]["surname"], phone_num = userdata[0]["phone_number"], users = mongodb_query.showAllusers_table())
	else:
		return render_template('register_page.html')




@app.route('/register', methods = ['GET','POST'])
def register():
	if request.method == "GET":
		if 'username' in session:
			return redirect(url_for("mainpage"))
		else:
			return render_template('register_page.html')
	elif request.method == "POST":
		if mongodb_query.create_user(request.form['username'], request.form['password'], request.form['name'], request.form['surname'], request.form['phone_number']):
			return redirect ('mainpage')
		else:
			flash("This username is already in use. Please try another one")
			return render_template('register_page.html')



@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect ('/')




@app.route('/changepass', methods = ['GET','POST'])
def changepass():
	if request.method == "POST":
		if 'username' in session:
			if request.form['new_password'] == request.form['new_password2']:
				if mongodb_query.change_pass(session['username'], request.form['old_password'], request.form['new_password']):
					flash("Password successfuly canged")
					return redirect(url_for("mainpage"))
				else:
					flash("Wrong old password")
					return render_template('changepass_page.html')
			else:
				flash("Passwords should be the same")
				return render_template('changepass_page.html')
	if request.method == "GET":
		if 'username' in session:
			return render_template('changepass_page.html')
		else:
			return redirect ('/')



#setting page allow to upload avatar
#			  redir to change password
#					to change name,surname,phone_num
@app.route('/settings', methods = ['GET'])
def settings():
	if request.method == "GET":
		if 'username' in session:
			userdata = mongodb_query.showUser_info(session['username'])[0]
			try:
				avatar =  mongo.db.users_table.find_one({'username':session['username']})['avatar']
				return render_template("setting_page.html", login = userdata["username"], name = userdata["name"], surname = userdata["surname"], phone_num = userdata["phone_number"], image=avatar)
			except KeyError:
				return render_template("setting_page.html", login = userdata["username"], name = userdata["name"], surname = userdata["surname"], phone_num = userdata["phone_number"])
		else:
			return render_template('register_page.html')


#allows to change name,surname
@app.route('/settings_change', methods = ['GET', 'POST'])
def settings_change_info():
	if request.method == "GET":
		if 'username' in session:
			userdata = mongodb_query.showUser_info(session['username'])[0]
			return render_template("settings_change.html", name = userdata["name"], surname = userdata["surname"], phone_num = userdata["phone_number"])
		else:
			return render_template('login_page.html')

	if request.method == "POST":
		if 'username' in session:
			userdata = mongodb_query.showUser_info(session['username'])[0]
			if mongodb_query.change_info(session['username'], request.form['name'], request.form['surname'], request.form['phone_number']):
				flash("information successfuly changed")
				return redirect(url_for("settings_change_info"))
			else:
				flash("something goes wrong, try again")
				return redirect(url_for("settings_change_info"))

#creating new service
#first page for add information about service
@app.route('/create_service', methods = ['GET', 'POST'])
def create_service():
	if request.method == "GET":
		if 'username' in session:
			return render_template("service_create.html")

		else:
			return render_template('login_page.html')
	#saves information and turns to next step
	if request.method == "POST":
		if 'username' in session:
			#print(request.form['name_service'])
			#print(request.form['additional_information'])
			print("HERE I AM")
			name_service = request.form['service_name']
			additional_information = request.form['service_descr']
			service_image = request.files['service_image']
			#print(base64.b64encode(service_image.read()).decode())
			id = mongodb_query.create_service(session['username'], name_service, additional_information, service_image)
			#save information to DB
			#next page | map select
			#sending ID throught the each page of service registration
			return redirect(url_for('set_address', id=id, lt=latitude,lg=longitude))
			#return render_template('map.html',apikey=maps_api_key, id=id, latitude=latitude,longitude=longitude)#map.html is my HTML file name



#creating new service
#second page for add coordinates about service
@app.route('/set_address', methods = ['GET', 'POST'])
def set_address(id=0, lt = 59.9138, lg = 30.3483):
	#showing updated map
	if request.method == "GET":
		if 'username' in session:
			id = request.args.get('id')
			lat = request.args.get('lt')
			long = request.args.get('lg')
			return render_template('map.html',apikey=maps_api_key, id=id, latitude=lat,longitude=long)#map.html is my HTML file name

		else:
			return render_template('login_page.html')

	#set new address
	if request.method == "POST":
		if 'username' in session:
			id = request.args.get('id')
			address = request.form['city']+' '+request.form['street']+' '+request.form['building_number']
			PARAMS['q'] = address
			# sending get request and saving the response as response object
			r = requests.get(url = maps_URL, params = PARAMS)
			data = r.json()
			latitude = data['items'][0]['position']['lat']
			longitude = data['items'][0]['position']['lng']
			print(latitude)
			print(longitude)
			return redirect(url_for('set_address', id=id, lt=latitude,lg=longitude))#map.html is my HTML file name



#creating new service
#just saving coordinates and redirects to date_select [redirect - NOT WORKING]
@app.route('/save_coordinate', methods = ['GET', 'POST'])
def save_coordinate(id = 0, lt=0, lg=0):
	if request.method == "GET":
		if 'username' in session:
			#save coordinates to DB
			id = request.args.get('id')
			lat = request.args.get('lt')
			long = request.args.get('lg')
			print(session['username'],lat, long)
			if mongodb_query.service_coordinates(id, session['username'], lat, long):
				return redirect(url_for('date_select', id=id))
			else:
				return redirect(url_for('create_service'))



#creating new service
#third page for add free time for advice service
@app.route('/date_select', methods = ['GET', 'POST'])
def date_select(id = 0):
	if request.method == "GET":
		if 'username' in session:
			id = request.args.get('id')
			return render_template('date_select.html', id=id)
		else:
			return render_template('login_page.html')
	if request.method == "POST":
		if 'username' in session:
			id = request.args.get('id')
			get_schedular = request.get_json()
			print(get_schedular)
			#ALSO SHOULD ASK about how much work takes time to split working hours
			#save date time to DB
			#check if everything ok then return created page
			set_schedular = dict() # prepare to send to mongo {date: time]}
			range_time = get_schedular.pop(0)
			for selected in get_schedular:
				data = selected.split("\t")
				data.pop(0)#deleting empty('') item
				time = (int(data[1].split("-")[1])-int(data[1].split('-')[0]))
				set_schedular[data[0]] = data[1]

			print(set_schedular)
			if mongodb_query.service_schedule(id, session['username'], set_schedular):
				print("SHOULD REDICRECT!!!!111")
				return redirect(url_for('service',id=id))
			else:
				return redirect(url_for('create_service'))
			#all done, save and set a number of service, call created page
			#get created id of service by session 'username'





#created service
#page with whole information about service and pick time
@app.route('/service', methods = ['GET', 'POST'])
def service(id = 1):

	if request.method == "GET":
		if 'username' in session:
			id = request.args.get('id')
			#get information about service from DB by id
			get_info = mongodb_query.service_info(id)
			if get_info:
				service_name = get_info["service_name"]
				service_information = get_info["addit_info"]
				master = get_info["username"]
				free_hours_on_selected_date = get_info["schedule"]
				coordinates = [get_info["lt"], get_info["lg"]]
				print("before rendering")
				#return redirect('login_page.html')
				return render_template('service.html',s_name=service_name, s_info=service_information, master = master, date = "08.05.20",hours=map(json.dumps, free_hours_on_selected_date))
			else:
				#there is not such service
				return render_template("mainpage")

	#used to select the date and should return time Todo
	if request.method == "POST":
		if 'username' in session:
			get_info = mongodb_query.service_info(id)
			if get_info:
				service_name = get_info["service_name"]
				service_information = get_info["addit_info"]
				master = get_info["username"]
				free_hours_on_selected_date = get_info["schedule"]
				coordinates = [get_info["lt"], get_info["lg"]]
				print("before rendering")
				#return redirect('login_page.html')
				return render_template('service.html',s_name=service_name, s_info=service_information, master = master, date = "08.05.20",hours=map(json.dumps, free_hours_on_selected_date))
			else:
				#there is not such service
				return render_template("mainpage")


#Finding list of services
@app.route('/find', methods = ['POST'])
def find_service(page = 1, filter = 'null'):
	#used for looking services
	if request.method == "POST":
		if 'username' in session:
			find_by = request.data.decode("utf-8")
			print("SMARI SUDA")
			filter = request.args.get('filter')
			#TODO: implement all charakteristic and then make right requests to DB
			print(filter)
			#TODO: check for int
			page = int(request.args.get('page'))-1
			count, result = mongodb_query.service_find(find_by, page)
			if count:
				print(result)
				print("HERE")

				return jsonify({'count':count, 'services':result})
				#return render_template('main_info.html',page=page, count=count, services=json.dumps(result))
			else:
				#there is no such service
				return render_template("mainpage")
	#used for next page view
	if request.method == "GET":
		if 'username' in session:
			find_by = request.data.decode("utf-8")



#uploading a picture from settings
@app.route('/up', methods = [ 'post'])
def upload_file():
	if 'username' in session:
		if request.method == 'POST':
			# check if the post request has the file part
			if 'file' not in request.files:
				flash('No file part')
				return redirect(url_for("mainpage"))
			file = request.files['file']
			# if user does not select file, browser also
			# submit an empty part without filename
			if file.filename == '':
				flash('No selected file')
				return redirect(url_for("mainpage"))
			if file:
				mongo.db.users_table.update_one({'username': session['username']}, {"$set":{'avatar':base64.b64encode(file.read()).decode()}})
				flash("Image uploaded")
			return redirect(url_for("mainpage"))
	else:
		return redirect ('/')







if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
