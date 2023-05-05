import pymongo

class DBHandler:
    def __init__(self, db_name):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]

    def signup(self, username, password):
        # check if the username is already taken
        if self.db["users"].find_one({"username": username}):
            return False
        
        # create a new user document
        user = {"username": username, "password": password}
        
        # insert the user document into the database
        result = self.db["users"].insert_one(user)
        
        return True

    def login(self, username, password):
        # check if the username exists in the database
        user = self.db["users"].find_one({"username": username})
        if not user:
            return False
        
        # check if the password matches
        if user["password"] != password:
            return False
        
        # create a new session document
        session = {"user_id": user["_id"]}
        
        # insert the session document into the database
        #result = self.db.sessions.insert_one(session)
        
        return True
    def logout(self, session_id):
        # delete the session document from the database
        result = self.db.sessions.delete_one({"_id": pymongo.ObjectId(session_id)})
        return result.deleted_count > 0
