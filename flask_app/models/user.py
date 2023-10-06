from flask_app.config.mysqlconnection import connectToMySQL 
from flask import flash
from flask_app.models import book

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        # connect to our specific db and query the database
        result = connectToMySQL('user-test').query_db(query)
        # convert all results from list of dictionaries 
        # to list of class objects
        users = []
        for user in result:
            users.append(cls(user))
        # return list of user class objects
        return users
    
    @classmethod
    def save(cls,data): 
        query = "INSERT INTO users(first_name, last_name, email, password, created_at,updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, Now(),Now());"
        return connectToMySQL('user-test').query_db(query, data)  
    
    # Get One User by ID
    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('user-test').query_db(query,data)
        print("one user:", result)
        return cls(result[0])
    
    @classmethod
    def get_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('user-test').query_db(query,data)
        # if user with this email doesn't exist, return false
        if len(result) < 1:
            return False
        # create class instance of user returned
        return cls(result[0])

    # Update User
    @classmethod
    def update(cls,data):
        query = """
            UPDATE users SET first_name = %(first_name)s, 
            last_name = %(last_name)s, email = %(email)s, 
            updated_at = Now() WHERE id = %(id)s;
        """
        return connectToMySQL("user-test").query_db(query,data)

    # Delete User

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL('user-test').query_db(query,data)
    
    @classmethod
    def get_users_w_books(cls):
        query = "SELECT * FROM users JOIN books ON users.id = books.user_id"
        results = connectToMySQL('user-test').query_db(query)
        print(results)

        if results:
            new_result = []
            for row in results:
                user = cls(row)
                data = {
                    "id":row['books.id'],
                    "title":row['title'],
                    "author":row['author'],
                    "num_pages":row['num_pages'],
                    'user_id':row['user_id'],
                    "created_at":row['books.created_at'],
                    "updated_at":row['books.updated_at']
                }

                user.books.append(book.Book(data))
                new_result.append(user)
            return new_result



                


    



    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['username']) < 3:
            flash("Hey username must be more than 3 characters long!")
            is_valid = False
        if len(user['email']) < 4:
            flash("Hey email must be more than 4 characters long!")
            is_valid = False
        return is_valid






        
