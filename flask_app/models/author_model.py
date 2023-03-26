from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book_model
from flask import flash
import re


class Authors:
    DB = "books_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books = []

    @classmethod
    def save_author(cls, data):
        query = """INSERT into authors
                (name)
                VALUES (%(name)s);

        """
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @classmethod
    def get_all_authors(cls):
        query = """SELECT * FROM authors"""
        results = connectToMySQL(cls.DB).query_db(query)

        authors = []

        for all_authors in results:
            authors.append (cls(all_authors))
        return authors

    @classmethod
    def unfavorited_authors(cls,data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN ( SELECT author_id FROM favorites WHERE book_id = %(id)s );"
        authors = []
        results = connectToMySQL(cls.DB).query_db(query,data)
        for row in results:
            authors.append(cls(row))
        return authors

    @classmethod     
    def add_favorite(cls, data):
        query = """ INSERT INTO favorites (author_id, book_id ) 
            VALUES (%(author_id)s, %(book_id)s)"""         
        return connectToMySQL(cls.DB).query_db(query, data)

    # @classmethod
    # def get_author(cls, data):
    #     query = """SELECT * FROM authors
    #             where id = %(id)s; """


    #     results = connectToMySQL(cls.DB).query_db(query, data)

    #     return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)

        # Creates instance of author object from row one
        author = cls(results[0])
        # append all book objects to the instances favorites list.
        for row in results:
            # if there are no favorites
            if row['books.id'] == None:
                break
            # common column names come back with specific tables attached
            data = {
                "id": row['books.id'],
                "title": row['title'],
                "num_of_pages": row['num_of_pages'],
                "created_at": row['books.created_at'],
                "updated_at": row['books.updated_at']
            }
            author.favorite_books.append(book_model.Books(data))
        return author









    # @classmethod
    # def get_by_email(cls,data):
    #     query = "SELECT * FROM users WHERE email = %(email)s;"
    #     result = connectToMySQL(cls.DB).query_db(query,data)

    #     if len(result) < 1:
    #         return False
    #     return cls(result[0])


    # @classmethod
    # def save(cls, data ):

    #     pw_hash = bcrypt.generate_password_hash(data['password'])
    #     data_dict = {
    #     "first_name": data['first_name'],
    #     "last_name": data['last_name'],
    #     "email": data['email'],
    #     "password" : pw_hash
    # }
    #     query = """
    #             INSERT into users 
    #             (first_name, last_name, email, password) 
    #             VALUES 
    #             ( %(first_name)s , %(last_name)s , %(email)s ,  %(password)s)
        
    #     """
    #     # #Deleted bottom two codes because I am now passinf data_dict. this is inteneded to replace data from controller. This will avoid your issue of not being able to hash a password and simply pass request.form
    #     # result = connectToMySQL(cls.DB).query_db(query,data)
    #     # return result
    #     result = connectToMySQL(cls.DB).query_db(query, data_dict)
    #     return result

    # @classmethod
    # def get_one(cls, data):
    #     query = """SELECT * FROM users WHERE id = %(id)s;"""
    #     results = connectToMySQL(cls.DB).query_db(query, data)

    #     return cls(results[0])

    # @staticmethod
    # def validate_user(form_data):
    #     is_valid = True
    #     data= { "email": form_data["email"]}
    #     valid_user = Users.get_by_email(data)

    #     if len(form_data["first_name"]) < 3:
    #         flash("First name must be at least 3 characters.", "register")
    #         is_valid = False
    #     if len(form_data["last_name"]) < 3:
    #         flash("Last name must be at least 3 characters.", "register")
    #         is_valid = False
    #     if not EMAIL_REGEX.match(form_data["email"]):
    #         flash ("Invalid email address.", "register")
    #         is_valid = False
    #     if valid_user:
    #         flash ("Email is already in use!.", "register")
    #         is_valid=False
    #     if len(form_data["password"]) < 8:
    #         flash ("Password must be at least 8 characters", "register")
    #         is_valid = False
    #     if form_data['conf_password'] != form_data['password']:
    #         flash("Password and confirm password must match!", "register")
    #         is_valid=False
        
    #     return is_valid

    # @staticmethod
    # def validate_login(form_data):
    #     is_valid= True
        
    #     data= { "email": form_data["login_email"]}
    #     valid_user = Users.get_by_email(data)
    #     if not valid_user:
    #         flash('Invalid Crendentials', "login")
    #         is_valid=False
    #     if valid_user:
    #         if not bcrypt.check_password_hash(valid_user.password, form_data['login_password']):
    #             flash('Invalid Credentials',"login")
    #             is_valid=False
        
    #     if len(form_data['login_email']) <1 and len(form_data['login_password']) <1:
    #         flash('Invalid Crendentials', "login")
    #         is_valid = False
    #     return is_valid