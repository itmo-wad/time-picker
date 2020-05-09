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
