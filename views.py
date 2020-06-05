""" Views file """

import os
#import json
import base64
import requests
from PIL import Image 				# To resize image
import secrets
import mongodb_query
from app import app, mongo
from forms import RegistrationForm, LoginForm, UpdateAccountForm, CreateServiceForm
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required
from flask import Flask, send_from_directory, request, flash, redirect, render_template, url_for, jsonify


maps_URL = "https://geocode.search.hereapi.com/v1/geocode"
maps_image_URL = "https://image.maps.ls.hereapi.com/mia/1.6/mapview"
maps_api_key = app.config["MAPS_API"]
get_coords_params = {'apikey':maps_api_key,'q':"Невский проспект"}#default address
#z params for zoom image
#w for request width image
latitude = 59.9138
longitude = 30.3483
get_image_params = {'c': str(latitude)+','+str(longitude), 'z':'16', 'w':"500", 'apiKey':maps_api_key} #example default params for requst img






services = [
{
	"owner": "user",
	"master_name": "Elena Sergeevna Sokolova",
	"service_name": "Barbershop666",
	"additional_info": "I'm the best in this. I want to became a famous barber and now i'm looking for my regular clints, that's why price so little.",
	"service_logo": "default.jpeg" },
{
	"owner": "user",
	"master_name": "Elena Sergeevna Sokolova",
	"service_name": "Barbershop666",
	"additional_info": "I'm the best in this. I want to became a famous barber and now i'm looking for my regular clints, that's why price so little.",
	"service_logo": "default.jpeg" },
]


# Register new user page
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('mainpage'))
	form = RegistrationForm()
	if form.validate_on_submit():
		# hash the password, add user to DB
		#hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		if mongodb_query.create_user(form.username.data, form.password.data, form.name.data, form.surname.data, form.phone_number.data):
			flash('Account was successfully created!', 'success')
			return redirect(url_for('login'))
		else:
			flash('This username is already taken. Please try another one.', 'danger')
	return render_template('register.html', title='Register', form=form)


# Login page
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('mainpage'))
	form = LoginForm()
	if form.validate_on_submit():
		# TODO:
		if mongodb_query.user_exists(form.username.data) and mongodb_query.user_credentials(form.username.data, form.password.data):
			# Create session for this user
			user = mongodb_query.User(list(mongo.db.users_table.find({"username": form.username.data}).limit(1))[0])
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('mainpage'))
		else:
			flash('Incorrect login or password!', 'danger')
	return render_template('login.html', title='Login', form=form)


# Logout
@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You were successfully logged out!', 'info')
	return redirect(url_for('login'))


# Main app page
@app.route('/mainpage')
@login_required
def mainpage():
	return render_template('mainpage.html')




# # Main app page
# @app.route('/mainpage')
# @login_required
# def mainpage():
# 	userdata = mongodb_query.showUser_info(current_user.username)
# 	name = userdata[0]["surname"] + " " + userdata[0]["name"]
# 	try:
# 		avatar = mongo.db.users_table.find_one({'username': current_user.username})['avatar']
# 		return render_template('main_info.html', name=name, image=avatar, phone_num=userdata[0]["phone_number"])
# 	except KeyError:
# 		return render_template('main_info.html', name=name, phone_num=userdata[0]["phone_number"])


# Save picture to filesystem
def save_picture(form_picture, out_size, folder):
	# Create random name for profile picture
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_picture.filename)
	picture_filename = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/content/', folder, picture_filename)
	output_size = (out_size, out_size)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_filename


# User settings page
@app.route('/account_info', methods=['GET', 'POST'])
@login_required
def account_info():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.profile_pic.data:
			profile_pic_file = save_picture(form.profile_pic.data, 125, 'profile_pics')
			current_user.profile_pic = profile_pic_file
			mongodb_query.profile_pic_update(current_user.username, current_user.profile_pic)
		# kostyl iz-za mongodb
		current_user.name = form.name.data
		current_user.surname = form.surname.data
		current_user.phone_number = form.phone_number.data
		if mongodb_query.user_update(current_user.username, current_user.name, current_user.surname, current_user.phone_number):
			flash('Your data has been updated!', 'success')
			return redirect(url_for('account_info'))
		else:
			flash('Something went wrong!', 'warning')
			return redirect(url_for('account_info'))
	elif request.method == 'GET':
		form.name.data = current_user.name
		form.surname.data = current_user.surname
		form.phone_number.data = current_user.phone_number
	avatar_img = url_for('static', filename='content/profile_pics/' + current_user.profile_pic)
	return render_template('account_info.html', title='Account info', avatar_img=avatar_img, form=form)




# @app.route('/changepass', methods = ['GET','POST'])
# def changepass():
# 	if request.method == "POST":
# 		if 'username' in session:
# 			if request.form['new_password'] == request.form['new_password2']:
# 				if mongodb_query.change_pass(session['username'], request.form['old_password'], request.form['new_password']):
# 					flash("Password successfuly canged")
# 					return redirect(url_for("mainpage"))
# 				else:
# 					flash("Wrong old password")
# 					return render_template('changepass_page.html')
# 			else:
# 				flash("Passwords should be the same")
# 				return render_template('changepass_page.html')
# 	if request.method == "GET":
# 		if 'username' in session:
# 			return render_template('changepass_page.html')
# 		else:
# 			return redirect ('/')



# @app.route('/created_services', methods = ["POST", "GET"])
# def created_services():
# 	if request.method == 'GET':
# 		return render_template('created_services.html')
# 	if request.method == 'POST':
# 		services = mongodb_query.get_services(session["username"])

# 		return jsonify({"services":services})


@app.route('/my_services')
@login_required
def my_services():
	#services = mongodb_query.get_user_services(current_user.username)
	logo_folder = '/content/service_pics/'
	return render_template('my_services.html', services=services, logo_folder=logo_folder)



@app.route('/test_create', methods = ["POST", "GET"])
@login_required
def test_create():
	form = CreateServiceForm()
	if request.method == 'POST':

		flash('Service successfully created!', 'success')
		return redirect(url_for('my_services'))
	return render_template('service_create.html', title='Create new service', form=form)




@app.route('/get_address_image', methods = ['POST'])
@login_required
def get_address_image():
	#showing updated map
	if current_user.is_authenticated:
		if request.method == "POST":
			#address used for request url to get coords
			address = request.form['city']+' '+request.form['street']+' '+request.form['building_num']
			#width used to requst image with the same width
			user_screen_width = request.form['width']
			get_coords_params['q'] = address

			r = requests.get(url = maps_URL, params = get_coords_params)
			data = r.json()
			latitude = data['items'][0]['position']['lat']
			longitude = data['items'][0]['position']['lng']
			get_image_params['c'] = str(latitude)+','+str(longitude)
			get_image_params['z'] = "16"#scale image
			get_image_params['apiKey'] = maps_api_key
			get_image_params['w'] = user_screen_width
			image = requests.get(url = maps_image_URL, params = get_image_params)
			print(image)


			return jsonify({"image": base64.b64encode(image.content).decode()})





# #setting page allow to upload avatar
# #			  redir to change password
# #					to change name,surname,phone_num
# @app.route('/settings', methods = ['GET'])
# def settings():
# 	if request.method == "GET":
# 		userdata = mongodb_query.showUser_info(current_user.username)[0]
# 		try:
# 			avatar =  mongo.db.users_table.find_one({'username': current_user})['avatar']
# 			return render_template("setting_page.html", login = userdata["username"], name = userdata["name"], surname = userdata["surname"], phone_num = userdata["phone_number"], image=avatar)
# 		except KeyError:
# 			return render_template("setting_page.html", login = userdata["username"], name = userdata["name"], surname = userdata["surname"], phone_num = userdata["phone_number"])



# #allows to change name,surname
# @app.route('/settings_change', methods = ['GET', 'POST'])
# def settings_change_info():
# 	if request.method == "GET":
# 		if 'username' in session:
# 			userdata = mongodb_query.showUser_info(session['username'])[0]
# 			return render_template("settings_change.html", name = userdata["name"], surname = userdata["surname"], phone_num = userdata["phone_number"])
# 		else:
# 			return render_template('login_page.html')

# 	if request.method == "POST":
# 		if 'username' in session:
# 			userdata = mongodb_query.showUser_info(session['username'])[0]
# 			if mongodb_query.change_info(session['username'], request.form['name'], request.form['surname'], request.form['phone_number']):
# 				flash("information successfuly changed")
# 				return redirect(url_for("settings_change_info"))
# 			else:
# 				flash("something goes wrong, try again")
# 				return redirect(url_for("settings_change_info"))



# #uploading a picture from settings
# @app.route('/up', methods = [ 'post'])
# def upload_file():
# 	if 'username' in session:
# 		if request.method == 'POST':
# 			# check if the post request has the file part
# 			if 'file' not in request.files:
# 				flash('No file part')
# 				return redirect(url_for("mainpage"))
# 			file = request.files['file']
# 			# if user does not select file, browser also
# 			# submit an empty part without filename
# 			if file.filename == '':
# 				flash('No selected file')
# 				return redirect(url_for("mainpage"))
# 			if file:
# 				mongo.db.users_table.update_one({'username': session['username']}, {"$set":{'avatar':base64.b64encode(file.read()).decode()}})
# 				flash("Image uploaded")
# 			return redirect(url_for("mainpage"))
# 	else:
# 		return redirect ('/')










#creating new service
#first page for add information about specialization
@app.route('/create_service', methods = ['GET', 'POST'])
def create_service(idc = 0):
	if request.method == "GET":
		if 'username' in session:
			idc = request.args.get('idc')
			if idc != None:
				return render_template("service_create_specialization.html")
			else:
				#todo check if service belongs username
				return render_template("service_create_specialization.html", idc = idc)

		else:
			return render_template('login_page.html')
	#saves information and turns to next step
	if request.method == "POST":
		if 'username' in session:
			idc = request.args.get('idc')
			name_service = request.form['service_name']
			additional_information = request.form['service_descr']
			service_image = request.files['service_image']
			if idc != None:
				print(idc)
				mongodb_query.change_service(idc, session['username'], name_service, additional_information, service_image)
				return redirect(url_for('created_services'))

			else:
				id = mongodb_query.create_service(session['username'], name_service, additional_information, service_image)
				#save information to DB
				#next page | map select
				#sending ID throught the each page of service registration
				if id != -1:
					return redirect(url_for('set_services', id=id))
				else:
					print("service already registered todo")
					return redirect(url_for('mainpage'))
		else:
			render_template("login_page.html")

#creating new service
#second page for add services that could be done by master
@app.route('/set_services', methods = ['GET', 'POST'])
def set_services(id = 0, idc = 0):
	if request.method == "GET":
		if 'username' in session:
			ids = request.args.get('ids')
			if ids != 0:
				id = request.args.get('id')
				return render_template("service_create_services.html", id=id)
			else:
				return render_template("service_create_services.html", ids=ids)
		else:
			render_template("login_page.html")

	if request.method == "POST":
		if 'username' in session:
			id = request.args.get('id')

			services_prices = request.get_json()
			services_names = []
			summ_prices = 0
			count = 0
			for name_service in services_prices:
				services_names.append(name_service)
				summ_prices += int(services_prices[name_service])
				count +=1

			middle_price = summ_prices/count

			#TODO: find out best way to store service names with prices

			if mongodb_query.set_services(id, session['username'], services_names, services_prices, middle_price):

				return redirect(url_for('set_address', id=id, lt=latitude,lg=longitude))
			else:
				return redirect(url_for('set_services',id=id))
		else:
			render_template("login_page.html")

#creating new service
#third page for add coordinates about service
@app.route('/set_address', methods = ['GET', 'POST'])
def set_address(id=0, lt = 59.9138, lg = 30.3483):
	#showing updated map
	if request.method == "GET":
		if 'username' in session:
				id = request.args.get('id')
				print(id)
				lat = request.args.get('lt')
				long = request.args.get('lg')
				return render_template('service_create_map.html',apikey=maps_api_key, id=id, latitude=lat,longitude=long)#map.html is my HTML file name

		else:
			return render_template('login_page.html')

	#set new address
	if request.method == "POST":
		if 'username' in session:
			id = request.args.get('id')
			address = request.form['city']+' '+request.form['street']+' '+request.form['building_number']
			get_coords_params['q'] = address
			# sending get request and saving the response as response object
			r = requests.get(url = maps_URL, params = get_coords_params)
			data = r.json()
			latitude = data['items'][0]['position']['lat']
			longitude = data['items'][0]['position']['lng']
			return redirect(url_for('set_address', id=id, lt=latitude,lg=longitude))#map.html is my HTML file name



#creating new service
#just saving coordinates and redirects to date_select [redirect - NOT WORKING]
@app.route('/save_coordinate', methods = ['GET', 'POST'])
def save_coordinate(id = 0, lt=0, lg=0):
	if request.method == "GET":
		if 'username' in session:
			#todo continue
			#save coordinates to DB
			id = request.args.get('id')
			lat = request.args.get('lt')
			long = request.args.get('lg')
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
			return render_template('service_create_date_select.html', id=id)
		else:
			return render_template('login_page.html')
	if request.method == "POST":
		if 'username' in session:
			id = request.args.get('id')
			get_schedular = request.get_json()
			#ALSO SHOULD ASK about how much work takes time to split working hours
			#save date time to DB
			#check if everything ok then return created page
			set_schedular = dict() # prepare to send to mongo {date: time]}
			range_time = get_schedular.pop(0)
			for selected in get_schedular:
				data = selected.split("\t")
				print(data)
				if data[0] == '':
					data.pop(0)#deleting empty('') item
				time = (int(data[1].split("-")[1])-int(data[1].split('-')[0]))
				set_schedular[data[0]] = data[1]

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
def find_specialist(key = 'specialist', page = 1, filter = 'null'):
	#used for looking services
	if request.method == "POST":
		if 'username' in session:
			keyword = request.data.decode("utf-8")
			filter = request.args.get('filter')
			find_by = request.args.get('key')
			#TODO: implement all charakteristic and then make right requests to DB
			print(filter)
			#TODO: check for int
			page = int(request.args.get('page'))-1
			if find_by == "specialist":
				count, result = mongodb_query.find(find_by, keyword, page, filter)
			elif find_by == "service":
				count, result = mongodb_query.find(find_by, keyword, page, filter)



			if count:
				return jsonify({'count':count, 'services':result})
				#return render_template('main_info.html',page=page, count=count, services=json.dumps(result))
			else:
				#there is no such service
				#Todo: show that no info found
				return render_template("mainpage")
	#used for next page view
	if request.method == "GET":
		if 'username' in session:
			find_by = request.data.decode("utf-8")

"""
#Finding list of services
@app.route('/find_service', methods = ['POST'])
def find_service(page = 1, filter = 'null'):
	#used for looking services
	if request.method == "POST":
		if 'username' in session:
			find_by = request.data.decode("utf-8")
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
"""




#Chat starts

#uses for return id from receiver
@app.route('/chat_with', methods = ["POST", "GET"])
@login_required
def chat_with(receiver = None):
	if current_user.is_authenticated:
		if request.method == 'GET':
			receiver_nick = request.args.get('receiver')
			chat_id = mongodb_query.get_chat_id(current_user.username, receiver_nick)
			return redirect(url_for('messanger', id=chat_id))

		if request.method == 'POST':
			return render_template('messanger.html', id = 0)

#opens chat with selected id
@app.route('/messanger', methods = ["POST", "GET"])
@login_required
def messanger(id = 0):
	if current_user.is_authenticated:
		if request.method == 'GET':
			chat_id = request.args.get('id')
			return render_template('messanger.html',id = chat_id)


		if request.method == 'POST':
			return render_template('messanger.html', id = 0)



@app.route('/get_messages', methods = ["POST"])
@login_required
def get_messages(id = 0):
	if current_user.is_authenticated:
		if request.method == 'POST':
			chat_id = request.args.get('id')
			messages = mongodb_query.get_messages(chat_id)
			print(messages)
			return jsonify({'data': messages})


@app.route('/get_new_messages', methods = ["POST"])
@login_required
def get_new_messages(id = 0):
	if current_user.is_authenticated:
		if request.method == 'POST':
			date = request.data.decode("utf-8").split(',')
			chat_id = request.args.get('id')
			#db.messages.find({"chat_id":1, 'date': {'$lt': ISODate("2020-05-30T18:52:19.069Z"), '$gte': ISODate("2020-05-30T18:49:55.077Z")}},  { "_id": 0} )
			request_time = datetime.strptime(date[0], '%Y-%m-%dT%H:%M:%S.%fZ')#datetime(2020, 5, 31, 9, 5, 9, 902785)#"Sun May 30 2020 18:49:55 GMT+0300"#
			last_update_time = datetime.strptime(date[1], '%Y-%m-%dT%H:%M:%S.%fZ')#datetime(2020, 5, 31, 9, 4, 25, 243362)#"Sun May 30 2020 18:52:19 GMT+0300"#
			new_messages = mongodb_query.get_new_messages(chat_id, current_user.username, request_time, last_update_time )

			return jsonify({'new_msgs': new_messages})


@app.route('/send_message', methods = ["POST"])
def send_message(id = 0):
	if current_user.is_authenticated:
		if request.method == 'POST':
			chat_id = request.args.get('id')
			message = request.data.decode("utf-8")
			date = datetime.utcnow()
			mongodb_query.send_message(chat_id, current_user.username, message, date)
			return jsonify(success=True)



@app.route('/chatlist', methods = ["POST"])
@login_required
def chatlist():
	if current_user.is_authenticated:
		if request.method == 'POST':
			#go for mongo
			chats = mongodb_query.get_list_chats(current_user.username)
			list_of_dict = []
			for chat in chats:#iterate through senders nicknames
				dict_messages = {}
				for nickname in chat["participants"]:
					if nickname != current_user.username:
						receiver = nickname
						break
				message = mongodb_query.get_last_message(current_user.username, receiver)
				if len(message) != 0:
					print(message)
					print(type(message))
					del message[0]['_id']
					dict_messages[receiver] = message[0]
				list_of_dict.append(dict_messages)

			return jsonify({"chats":list_of_dict})


#Chat ends











# ==========================================================================================
# All functions for testing will be placed BELOW

# #it used just for testing to see each registered user
# @app.route('/showregistered', methods = ['GET','POST'])
# def showregistered():
# 	if 'username' in session:
# 		userdata = mongodb_query.showUser_info(session['username'])
# 		try:
# 			avatar =  mongo.db.users_table.find_one({'username':session['username']})['avatar']
# 			return render_template("setting_page.html", login = userdata[0]["login"], name = userdata[0]["name"], surname = userdata[0]["surname"], phone_num = userdata[0]["phone_number"], image=avatar, users = mongodb_query.showAllusers_table())
# 		except KeyError:
# 			return render_template("setting_page.html", login = userdata[0]["username"], name = userdata[0]["name"], surname = userdata[0]["surname"], phone_num = userdata[0]["phone_number"], users = mongodb_query.showAllusers_table())
# 	else:
# 		return render_template('register_page.html')


# @app.route('/who_am_i', methods = ["POST"])
# def who_am_i():
# 	if 'username' in session:
# 		if request.method == 'POST':
# 			return jsonify({'nick': session['username']})




# @app.route('/check', methods = ["POST", "GET"])
# def check():
# 	if 'username' in session:
# 		mongodb_query.check_func_mongo()
# 		jsonify(success=True)




# def mainpage():
# 	if request.method == "GET":
# 		if 'username' in session:
# 			userdata = mongodb_query.showUser_info(session['username'])
# 			name = userdata[0]["surname"]+" "+userdata[0]["name"]
# 			try:
# 				avatar =  mongo.db.users_table.find_one({'username':session['username']})['avatar']
# 				return render_template('main_info.html', name = name, image=avatar, phone_num = userdata[0]["phone_number"])
# 			except KeyError:
# 				return render_template('main_info.html', name = name, phone_num = userdata[0]["phone_number"])
# 		else:
# 			return redirect ('/')






# @app.route('/login', methods = ['GET','POST'])
# def login():
# 	if request.method == "POST":
# 		if mongodb_query.user_exist(request.form['username'], request.form['password']):
# 			session['username'] = request.form['username']
# 			return redirect('mainpage')
# 		else:
# 			flash("Incorrect login or password!")
# 			return render_template('login_page.html')
# 	elif request.method == "GET":
# 		if 'username' in session:
# 			return redirect(url_for("mainpage"))
# 	return render_template('login_page.html')





# @app.route('/register', methods = ['GET','POST'])
# def register():
# 	if request.method == "GET":
# 		if 'username' in session:
# 			return redirect(url_for("mainpage"))
# 		else:
# 			return render_template('register_page.html')
# 	elif request.method == "POST":
# 		if mongodb_query.create_user(request.form['username'], request.form['password'], request.form['name'], request.form['surname'], request.form['phone_number']):
# 			return redirect ('mainpage')
# 		else:
# 			flash("This username is already in use. Please try another one")
# 			return render_template('register_page.html')
