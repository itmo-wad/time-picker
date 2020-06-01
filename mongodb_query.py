"""
DB preparation:
> db.createCollection("counters")
> db.counters.insert({_id:"productid",sequence_value:0})
> function getNextSequenceValue(sequenceName){

   var sequenceDocument = db.counters.findAndModify({
	  query:{_id: sequenceName },
	  update: {$inc:{sequence_value:1}},
	  new:true
   });

   return sequenceDocument.sequence_value;
}



I don't know why, but when DB is not in use some time, then function delete automaticly
Need to create again
function getNextSequenceValue(sequenceName){ var sequenceDocument = db.counters.findAndModify({ query:{_id: sequenceName }, update: {$inc:{sequence_value:1}}, new:true }); return sequenceDocument.sequence_value; }
"""
import re
import views
import base64




def user_exist(login, password):
	user = list(views.mongo.db.users_table.find({"username":login.lower(), "password":password}).limit(1))
	if user:
		return True
	else:
		return False


def create_user(login, password, name, surname, phone_number):
	user = list(views.mongo.db.users_table.find({"username":login.lower()}).limit(1))
	if user:
		return False
	else:
		views.mongo.db.users_table.insert({"username":login.lower(),"password":password, "name":name, "surname":surname, "phone_number":phone_number})
		return True


#returns list [username, password, name, surname, phone_number]
def showUser_info(login):
	user = list(views.mongo.db.users_table.find({"username":login.lower()}).limit(1))
	return user


def showAllusers_table():
	users_table = views.mongo.db.users_table.find({})
	return users_table


def change_pass(username, old_password, new_password):
	if user_exist(username, old_password):
		views.mongo.db.users_table.update({"username":username.lower()},{"$set":{"username":username.lower(),"password":new_password}})
		return True
	else:
		return False

def change_info(username, name, surname, phone_num):
	user = list(views.mongo.db.users_table.find({"username":username.lower()}).limit(1))
	if user:
		views.mongo.db.users_table.update({"username":username.lower()},{"$set":{"username":username.lower(),"name":name, "surname":surname, "phone_number":phone_num}})
		return True
	else:
		return False


#service creation
def create_service(login, service_name, addit_info, image):
	service_exsist = list(views.mongo.db.services.find({"username":login.lower(), "service_name": service_name}).limit(1))
	if service_exsist:
		print("#TODO service already registered with this login and service name")
		id = list(views.mongo.db.services.find({"username":login.lower(), "service_name": service_name}).limit(1))[0]
		return id
	else:
		#next_id = views.mongo.db.eval("getNextSequenceValue('productid')") #think it s not working with mlab
		print("id")
		#print(next_id)
		id = 9 #vremenniy kostil
		views.mongo.db.services.insert({"_id":id, "username":login.lower(), "service_name": service_name, "addit_info": addit_info, "service_logo": base64.b64encode(image.read()).decode()})
		return id

def set_services(id, login, services_names, services_prices, middle_price):
		#TODO: check if cant do int(id)?

		#check if service is belongs to login
		service_belong = list(views.mongo.db.services.find({"_id":int(id), "username":login.lower()}))[0]
		if service_belong:
			views.mongo.db.services.update({"_id":int(id), "username":login.lower()}, {"_id":int(service_belong["_id"]), "username":service_belong["username"], "service_name": service_belong["service_name"], "addit_info": service_belong["addit_info"], "service_logo":service_belong["service_logo"], "services_names":services_names, "services_prices":services_prices, "middle_price":middle_price})
			return True
		else:
			return False

def service_coordinates(id, login, lt, lg):
	#TODO: check if cant do int(id)?

	#check if service is belongs to login
	service_belong = list(views.mongo.db.services.find({"_id":int(id), "username":login.lower()}))[0]
	if service_belong:
		print("begin")
		views.mongo.db.services.update({"_id":int(id), "username":login.lower()}, {"_id":int(service_belong["_id"]), "username":service_belong["username"], "service_name": service_belong["service_name"], "addit_info": service_belong["addit_info"], "service_logo":service_belong["service_logo"], "services_names":service_belong["services_names"], "services_prices":service_belong["services_prices"], "middle_price":service_belong["middle_price"], "lt":lt, "lg":lg})
		print("finish")
		return True
	else:
		print("#TODO service not exsist go to first step of regidtration || hackers gonna suck1!")
		return False

def service_schedule(id, login, schedular):
	#TODO: check if cant do int(id)?

	#check if service is belongs to login
	print(schedular)
	service_belong = list(views.mongo.db.services.find({"_id":int(id), "username":login.lower()}))[0]
	if service_belong:
		views.mongo.db.services.update({"_id":int(id), "username":login.lower()}, {"_id":service_belong["_id"], "username":service_belong["username"], "service_name": service_belong["service_name"], "addit_info": service_belong["addit_info"], "service_logo":service_belong["service_logo"], "services_names":service_belong["services_names"], "services_prices":service_belong["services_prices"], "middle_price":service_belong["middle_price"], "lt":service_belong["lt"], "lg":service_belong["lg"], "schedule":schedular})
		return True
	else:
		print("#TODO service not exsist go to first step of registration || hackers gonna suck1!")
		return False

def service_info(id):
	#Returns info about service from database
	service = list(views.mongo.db.services.find({"_id":int(id)}))[0]
	if service:
		return service
	else:
		return false


def find(find_by, keyword, page, filter):
	services_on_page = 3
	if find_by == "specialist":

		count_of_service = len(list(views.mongo.db.services.find({"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE)})))
		if filter == 'null':
			services = list(views.mongo.db.services.find({"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE) }).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Lowest price':
			print("sorted by lowest price")
			services = list(views.mongo.db.services.find({ "$query": {"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE)}, "$orderby": { "middle_price" : 1 }}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Closest destination':
			services = list(views.mongo.db.services.find({"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE) }).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'High rating':
			services = list(views.mongo.db.services.find({ "$query": {"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE) }, "$orderby": { "rating" : -1 }}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Closest time':
			services = list(views.mongo.db.services.find({"service_name":re.compile('.*'+keyword+'.*', re.IGNORECASE) }).skip(services_on_page*int(page)).limit(services_on_page))
	elif find_by == "service":
		count_of_service = len(list(views.mongo.db.services.find({"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)})))
		if filter == 'null':
			services = list(views.mongo.db.services.find({"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Lowest price':
			services = list(views.mongo.db.services.find({ "$query": {"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)}, "$orderby": { "middle_price" : 1 }}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Closest destination':
			services = list(views.mongo.db.services.find({"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'High rating':
			services = list(views.mongo.db.services.find({ "$query": {"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)}, "$orderby": { "rating" : -1 }}).skip(services_on_page*int(page)).limit(services_on_page))
		elif filter == 'Closest time':
			services = list(views.mongo.db.services.find({"services_names":re.compile('.*'+keyword+'.*', re.IGNORECASE)}).skip(services_on_page*int(page)).limit(services_on_page))

	return count_of_service, services



#for messanger

def get_list_chats(nickname):
	chats = list(views.mongo.db.chats.find({"participants":nickname}))
	return chats

def get_last_message(sender, receiver):
	chat_id = get_chat_id(sender, receiver)
	message = list(views.mongo.db.messages.find({ "$query": {"chat_id":chat_id}, "$orderby": { "date" : -1 }}))

	return message

def get_chat_id(sender_nick, receiver_nick):
	check = [sender_nick, receiver_nick]
	check = sorted(check)
	chat_exist = list(views.mongo.db.chats.find({"participants":check}))
	if chat_exist:
		return chat_exist[0]["chat_id"]
	else:
		#next_id = views.mongo.db.eval("getNextSequenceValue('chatID')") #think it s not working with mlab
		print("id")
		#print(next_id)
		chat_id = 2 #vremenniy kostil
		views.mongo.db.chats.insert({"chat_id":chat_id,"participants":check})
		return chat_id


def send_message(chat_id, sender, message, date):
	#chat_id = get_chat_id(sender, receiver)
	views.mongo.db.messages.insert({"sender":sender,"chat_id":int(chat_id), "message_body":message, "date":date})



def get_messages(chat_id):
	messages = list(views.mongo.db.messages.find({"chat_id":int(chat_id)}, { "_id": 0}))
	return messages



def get_new_messages(chat_id, username, start_time, end_time):
	#messages = list(views.mongo.db.messages.find({"chat_id":chat_id, 'date': {'$lt': {'$dateFromString': {'dateString': start_time}}, '$gte': {'$dateFromString': {'dateString': end_time}}}},  { "_id": 0} ))
	#messages = list(views.mongo.db.messages.find({'date': {'$gte': end_time}},  { "_id": 0} ))

	messages = list(views.mongo.db.messages.find({"chat_id":int(chat_id), 'date': {'$lt': start_time, '$gte': end_time}},  { "_id": 0} ))
	return messages


def get_services(username):
    services = list(views.mongo.db.services.find({"username":username }))
    return services
