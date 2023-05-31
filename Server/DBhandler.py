import pymongo

class DBHandler:
    def __init__(self, db_name):
        #connect to a mongoDB server.   
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]

    def signup(self, username, password):
        # check if the username is already taken
        if self.db["users"].find_one({"Username": username}):
            return False
        
        # create a new user document
        user = {"Username": username, "Password": password}
        
        # insert the user document into the database
        result = self.db["users"].insert_one(user)
        
        return True
    
    def getAllUserPassword(self, username):
        passwords = self.db["passwords"].find({"Owner": username})
        password_lists = list(passwords)
        for password in password_lists:
            del password['_id']
        print(password_lists)
        return password_lists

    def login(self, username, password):
        # check if the username exists in the database
        user = self.db["users"].find_one({"Username": username})
        if not user:
            return False
        
        # check if the password matches
        if user["Password"] != password:
            return False
        
        # create a new session document
        #session = {"user_id": user["_id"]}
        
        # insert the session document into the database
        #result = self.db.sessions.insert_one(session)
        
        return True
        
    def logout(self, session_id):
        # delete the session document from the database
        result = self.db.sessions.delete_one({"_id": pymongo.ObjectId(session_id)})
        return result.deleted_count > 0
    
    def insert_password(self, json_info):
        #if self.db["passwords"].find_one({"Password": json_info["Password"], "Owner": json_info["Owner"]}):
        #    return False

        new_pass = {"Url": json_info["Url"], "Password": json_info["Password"], "Owner": json_info["Owner"]}
        result = self.db["passwords"].insert_one(new_pass)

        return True

         
