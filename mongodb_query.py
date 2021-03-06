"""

Structure of DB:

1. users_table - store info about users
    - username : str
    - password : str
    - name : str
    - surname : str
    - phone_number : str
    - avatar : str

2. services - store info about created services
    - _id: int  (to delete ?)
    - username: str  (of creator)
    - service_name: str
    - addit_info: str
    - service_logo: str (b64)
    - services_names: list<str>  (store list of provided services)
    - services_prices: dict<str:int>   (store reference to price of service)
    - middle_price: int
    - "lt": str
    - "lg": str
    - schedule: dict<str:list<dict<str:str>>>
        ex:{"06.06.20": [{"10:00 - 11:00": "busy"}, {"11:00 - 12:00": "availble"}], "07.06.20": [{"10:00 - 11:00": "busy"}, {"11:00 - 12:00": "busy"}]}

#Chat
3. chats - store routing info
    - chat_id: int
    - participants: list<str>
        ex: "participants": [ "admin", "user" ]

"""
import re
import base64
from flask_login import UserMixin
from app import mongo, login_manager


# User class
class User(UserMixin):
	profile_pic = 'default.jpg'
	email = 'default_email@example.com'
	created_servoces = []
	# Create class properties from dictionary
	# User.key returns value
	def __init__(self, dictionary):
		self.__dict__.update(dictionary)

	def get_id(self):
		try:
			return self.username
		except AttributeError:
			raise NotImplementedError('No `username` attribute - override `get_id`')


# User loader
@login_manager.user_loader
def load_user(username):
	# Returned from DB list with user's data
	user_list = list(mongo.db.users_table.find({"username": username}).limit(1))
	# If this user exists
	if len(user_list) > 0:
		# Manage session
		return User(user_list[0])
	else:
		# User is not logged in
		return None


# Function to check if username already exists
def user_exists(username):
	user = mongo.db.users_table.find_one({"username": username.lower()})
	if user:
		return True
	else:
		return False


# Function to check credentials
# returns True if pair (login, password) is the same as in DB
def user_credentials(login, password):
	user = list(mongo.db.users_table.find({"username":login.lower(), "password":password}).limit(1))
	if user:
		return True
	else:
		return False


# Function to update user account info
def user_update(username, name, surname, phone_num):
	if user_exists(username):
		mongo.db.users_table.update({"username": username.lower()},
									{"$set": {"username": username.lower(),
											  "name": name,
											  "surname": surname,
											  "phone_number": phone_num
											  }
									})
		return True
	else:
		return False


# Store picture in filesystem, store filename in DB
def profile_pic_update(username, pic_filename):
	if user_exists(username):
		mongo.db.users_table.update_one({'username': username.lower()},
										{"$set": {'profile_pic': pic_filename}
										})
		return True
	else:
		return False


# def user_exist(login, password):
# 	user = list(mongo.db.users_table.find({"username":login.lower(), "password":password}).limit(1))
# 	if user:
# 		return True
# 	else:
# 		return False

# Create user on registration
def create_user(username, password, name, surname, phone_number):
	if user_exists(username):
		return False
	else:
		mongo.db.users_table.insert({"username": username.lower(),
									 "password": password,
									 "name": name,
									 "surname": surname,
									 "phone_number": phone_number
									})
		return True


#returns list [username, password, name, surname, phone_number]
def get_user_info(username):
	return list(mongo.db.users_table.find({"username": username.lower()}).limit(1))


# Get services created by user
def get_user_services(username):
	return list(mongo.db.services.find({"owner": username.lower()}))


# Get all services from collection
def get_all_services():
	return list(mongo.db.services.find())


#service creation
def create_service(owner, service_id, service_name, master_name, addit_info, service_logo, services_prices, coords, dates):
	mongo.db.services.insert({"owner": owner.lower(),
							  "service_id": service_id,
							  "service_name": service_name,
							  "master_name": master_name,
							  "addit_info": addit_info,
							  "service_logo": service_logo,
							  "services_prices": services_prices,
							  "coords": coords,
							  "dates": dates
							  })
	return True


# Get service by id
def get_service_by_id(service_id):
	return list(mongo.db.services.find({"service_id": service_id}).limit(1))





# #returns list [username, password, name, surname, phone_number]
# def showUser_info(login):
# 	user = list(mongo.db.users_table.find({"username": login.lower()}).limit(1))
# 	return user


# def showAllusers_table():
# 	users_table = mongo.db.users_table.find({})
# 	return users_table


def change_pass(username, old_password, new_password):
	if user_exist(username, old_password):
		mongo.db.users_table.update({"username":username.lower()},{"$set":{"username":username.lower(),"password":new_password}})
		return True
	else:
		return False

# def change_info(username, name, surname, phone_num):
# 	user = list(mongo.db.users_table.find({"username":username.lower()}).limit(1))
# 	if user:
# 		mongo.db.users_table.update({"username":username.lower()},{"$set":{"username":username.lower(),"name":name, "surname":surname, "phone_number":phone_num}})
# 		return True
# 	else:
# 		return False


# #service creation
# def create_service(login, service_name, addit_info, image):
# 	service_exsist = list(mongo.db.services.find({"username":login.lower(), "service_name": service_name}).limit(1))
# 	if service_exsist:
# 		print("#TODO service already registered with this login and service name")
# 		id = list(mongo.db.services.find({"username":login.lower(), "service_name": service_name}).limit(1))[0]
# 		id = -1
# 		return id
# 	else:
# 		#next_id = mongo.db.eval("getNextSequenceValue('productid')") #think it s not working with mlab
# 		print("id")
# 		#print(next_id)
# 		id = 16 #vremenniy kostil
# 		mongo.db.services.insert({"_id":id, "username":login.lower(), "service_name": service_name, "addit_info": addit_info, "service_logo": base64.b64encode(image.read()).decode()})
# 		return id




def change_service(idc, username, name_service, addit_info, service_image):
	#query is not working
	mongo.db.services.update({"_id":idc, "username":username.lower()}, {"_id":idc, "username":username.lower(), "service_name": name_service, "addit_info": addit_info, "service_logo": base64.b64encode(service_image.read()).decode()})

def set_services(id, login, services_names, services_prices, middle_price):
		#TODO: check if cant do int(id)?

		#check if service is belongs to login
		service_belong = list(mongo.db.services.find({"_id":int(id), "username":login.lower()}))[0]
		if service_belong:
			mongo.db.services.update({"_id":int(id), "username":login.lower()}, {"_id":int(service_belong["_id"]), "username":service_belong["username"], "service_name": service_belong["service_name"], "addit_info": service_belong["addit_info"], "service_logo":service_belong["service_logo"], "services_names":services_names, "services_prices":services_prices, "middle_price":middle_price})
			return True
		else:
			return False

def service_coordinates(id, login, lt, lg):
	#TODO: check if cant do int(id)?

	#check if service is belongs to login
	service_belong = list(mongo.db.services.find({"_id":int(id), "username":login.lower()}))[0]
	if service_belong:
		print("begin")
		mongo.db.services.update({"_id":int(id), "username":login.lower()}, {"_id":int(service_belong["_id"]), "username":service_belong["username"], "service_name": service_belong["service_name"], "addit_info": service_belong["addit_info"], "service_logo":service_belong["service_logo"], "services_names":service_belong["services_names"], "services_prices":service_belong["services_prices"], "middle_price":service_belong["middle_price"], "lt":lt, "lg":lg})
		print("finish")
		return True
	else:
		print("#TODO service not exsist go to first step of regidtration || hackers gonna suck1!")
		return False

def service_schedule(id, login, schedular):
	#TODO: check if cant do int(id)?

	#check if service is belongs to login
	print(schedular)
	service_belong = list(mongo.db.services.find({"_id":int(id), "username":login.lower()}))[0]
	if service_belong:
		mongo.db.services.update({"_id":int(id), "username":login.lower()}, {"_id":service_belong["_id"], "username":service_belong["username"], "service_name": service_belong["service_name"], "addit_info": service_belong["addit_info"], "service_logo":service_belong["service_logo"], "services_names":service_belong["services_names"], "services_prices":service_belong["services_prices"], "middle_price":service_belong["middle_price"], "lt":service_belong["lt"], "lg":service_belong["lg"], "schedule":schedular})
		return True
	else:
		print("#TODO service not exsist go to first step of registration || hackers gonna suck1!")
		return False

def service_info(id):
	#Returns info about service from database
	service = list(mongo.db.services.find({"_id":int(id)}))[0]
	if service:
		return service
	else:
		return false


def find(find_by, keyword, page, filter):
	services_on_page = 3
	if find_by == "specialist":

		count_of_service = len(list(mongo.db.services.find({"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE)})))
		if filter == 'null':
			services = list(mongo.db.services.find({"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE) }).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Lowest price':
			print("sorted by lowest price")
			services = list(mongo.db.services.find({ "$query": {"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE)}, "$orderby": { "middle_price" : 1 }}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Closest destination':
			services = list(mongo.db.services.find({"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE) }).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'High rating':
			services = list(mongo.db.services.find({ "$query": {"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE) }, "$orderby": { "rating" : -1 }}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Closest time':
			services = list(mongo.db.services.find({"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE) }).skip(services_on_page*int(page)).limit(services_on_page))
	elif find_by == "service":
		count_of_service = len(list(mongo.db.services.find({"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)})))
		if filter == 'null':
			services = list(mongo.db.services.find({"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Lowest price':
			services = list(mongo.db.services.find({ "$query": {"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)}, "$orderby": { "middle_price" : 1 }}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Closest destination':
			services = list(mongo.db.services.find({"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'High rating':
			services = list(mongo.db.services.find({ "$query": {"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)}, "$orderby": { "rating" : -1 }}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Closest time':
			services = list(mongo.db.services.find({"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)}).skip(services_on_page*int(page)).limit(services_on_page))

	return count_of_service, services



#for messanger

def get_list_chats(nickname):
	chats = list(mongo.db.chats.find({"participants":nickname}))
	return chats

def get_last_message(sender, receiver):
	chat_id = get_chat_id(sender, receiver)
	message = list(mongo.db.messages.find({ "$query": {"chat_id":chat_id}, "$orderby": { "date" : -1 }}))

	return message

def get_chat_id(sender_nick, receiver_nick):
	check = [sender_nick, receiver_nick]
	check = sorted(check)
	chat_exist = list(mongo.db.chats.find({"participants":check}))
	if chat_exist:
		return chat_exist[0]["chat_id"]
	else:
		#next_id = mongo.db.eval("getNextSequenceValue('chatID')") #think it s not working with mlab
		print("id")
		#print(next_id)
		chat_id = 2 #vremenniy kostil
		mongo.db.chats.insert({"chat_id":chat_id,"participants":check})
		return chat_id


def send_message(chat_id, sender, message, date):
	#chat_id = get_chat_id(sender, receiver)
	mongo.db.messages.insert({"sender":sender,"chat_id":int(chat_id), "message_body":message, "date":date})



def get_messages(chat_id):
	messages = list(mongo.db.messages.find({"chat_id":int(chat_id)}, { "_id": 0}))
	return messages



def get_new_messages(chat_id, username, start_time, end_time):
	#messages = list(mongo.db.messages.find({"chat_id":chat_id, 'date': {'$lt': {'$dateFromString': {'dateString': start_time}}, '$gte': {'$dateFromString': {'dateString': end_time}}}},  { "_id": 0} ))
	#messages = list(mongo.db.messages.find({'date': {'$gte': end_time}},  { "_id": 0} ))

	messages = list(mongo.db.messages.find({"chat_id":int(chat_id), 'date': {'$lt': start_time, '$gte': end_time}},  { "_id": 0} ))
	return messages


# def get_services(username):
# 	services = list(mongo.db.services.find({"username":username }))
# 	return services
