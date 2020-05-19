from flask import Flask, send_from_directory, request, flash, redirect, session, url_for
from flask import render_template
from flask_pymongo import PyMongo
import os
import mongodb_query
import base64
import requests
import json



app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)



maps_URL = "https://geocode.search.hereapi.com/v1/geocode"
maps_api_key = os.environ.get("HERE_API_KEY")
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
			print(request.form['name_service'])
			print(request.form['additional_information'])
			#save information to DB
			#next page | map select
			return render_template('map.html',apikey=maps_api_key,latitude=latitude,longitude=longitude)#map.html is my HTML file name


#creating new service
#second page for add coordinates about service
@app.route('/set_address', methods = ['GET', 'POST'])
def set_address(lt = 59.9138, lg = 30.3483):
	#showing updated map
	if request.method == "GET":
		if 'username' in session:
			lat = request.args.get('lt')
			long = request.args.get('lg')
			return render_template('map.html',apikey=maps_api_key,latitude=lat,longitude=long)#map.html is my HTML file name

		else:
			return render_template('login_page.html')

	#set new address
	if request.method == "POST":
		if 'username' in session:
			PARAMS['q'] = request.form['address']
			# sending get request and saving the response as response object
			r = requests.get(url = maps_URL, params = PARAMS)
			data = r.json()
			latitude = data['items'][0]['position']['lat']
			longitude = data['items'][0]['position']['lng']
			print(latitude)
			print(longitude)
			return redirect(url_for('set_address',lt=latitude,lg=longitude))#map.html is my HTML file name



#creating new service
#just saving coordinates and redirects to date_select [redirect - NOT WORKING]
@app.route('/save_coordinate', methods = ['GET', 'POST'])
def save_coordinate(lt=0, lg=0):
	if request.method == "GET":
		if 'username' in session:
			#save coordinates to DB
			lat = request.args.get('lt')
			long = request.args.get('lg')
			print(session['username'],lat, long)
			return redirect(url_for('date_select'))



#creating new service
#third page for add free time for advice service
@app.route('/date_select', methods = ['GET', 'POST'])
def date_select():
	if request.method == "GET":
		if 'username' in session:
			return render_template('date_select.html')
		else:
			return render_template('login_page.html')
	if request.method == "POST":
		if 'username' in session:
			req = request.get_json()
			print(req)
			#ALSO SHOULD ASK about how much work takes time to split working hours
			#save date time to DB
			#check if everything ok then return created page

			#all done, save and set a number of service, call created page
			#get created id of service by session 'username'
			return redirect(url_for('service',id=1))




#created service
#page with whole information about service and pick time
@app.route('/service', methods = ['GET', 'POST'])
def service(id = 1):

	if request.method == "GET":
		if 'username' in session:
			#get information about service from DB by id
			service_name = "Barber"
			service_information = "Do the best, very fast, low cost."
			master = "Ivanov Ivan"
			free_hours_on_selected_date = ["10-12"]
			print("before rendering")
			#return redirect('login_page.html')
			return render_template('service.html',s_name=service_name, s_info=service_information, master = master, date = "08.05.20",hours=map(json.dumps, free_hours_on_selected_date))

	#used to change the date of time select
	if request.method == "POST":
		if 'username' in session:
			service_name = "Barber"
			service_information = "Do the best, very fast, low cost."
			master = "Ivanov Ivan"

			day = request.get_json()
			#selected day to show work hours
			print(day)
			#ask db about work hours on date
			free_hours_on_selected_date = ["10-11","11-12", "12-13"]

			return render_template('service.html',s_name=service_name, s_info=service_information, master = master, date = day, hours=map(json.dumps, free_hours_on_selected_date))



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
