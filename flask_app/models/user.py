from flask_app.config.mysqlconnection import connectToMySQL 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.age = data['age']
        self.country = data['country']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        # connect to our specific db and query the database
        result = connectToMySQL('userz').query_db(query)
        # convert all results from list of dictionaries 
        # to list of class objects
        users = []
        for user in result:
            users.append(cls(user))
        # return list of user class objects
        return users
    
    @classmethod
    def save(cls,data): 
        query = "INSERT INTO users(username,email,age,country) VALUES(%(username)s,%(email)s,%(age)s,%(country)s)" 
        return connectToMySQL('userz').query_db(query,data)  
    
    # Get One User by ID
    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('userz').query_db(query,data)
        print("one user:", result)
        return cls(result[0])

    # Update User
    @classmethod
    def update(cls,data):
        query = """UPDATE users SET username=%(username)s, 
        email=%(email)s,age=%(age)s,country=%(country)s WHERE id = %(id)s
        """
        return connectToMySQL('userz').query_db(query,data)

    # Delete User

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL('userz').query_db(query,data)





        
