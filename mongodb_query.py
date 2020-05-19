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
import views




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
def create_service(login, service_name, addit_info):
	service_exsist = list(views.mongo.db.services.find({"username":login.lower(), "service_name": service_name}).limit(1))
	if service_exsist:
		print("#TODO service already registered with this login and service name")
		id = list(views.mongo.db.services.find({"username":login.lower(), "service_name": service_name}).limit(1))[0]
		return id
	else:
		#id = views.mongo.db.eval("getNextSequenceValue('productid')") think it s not working with mlab
		id = 8 #vremenniy kostil
		views.mongo.db.services.insert({"_id":id, "username":login.lower(), "service_name": service_name, "addit_info": addit_info})
		return id


def service_coordinates(id, login, lt, lg):
	#TODO: check if cant do int(id)?

	#check if service is belongs to login
	service_belong = list(views.mongo.db.services.find({"_id":int(id), "username":login.lower()}))[0]
	if service_belong:
		print("begin")
		views.mongo.db.services.update({"_id":int(id), "username":login.lower()}, {"_id":int(service_belong["_id"]), "username":service_belong["username"], "service_name": service_belong["service_name"], "addit_info": service_belong["addit_info"], "lt":lt, "lg":lg})
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
		views.mongo.db.services.update({"_id":int(id), "username":login.lower()}, {"_id":service_belong["_id"], "username":service_belong["username"], "service_name": service_belong["service_name"], "addit_info": service_belong["addit_info"], "lt":service_belong["lt"], "lg":service_belong["lg"], "schedule":schedular})
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
