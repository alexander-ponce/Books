from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author_model
from flask_app.models import book_model
from flask import flash


class Books:
    DB = "books_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_with_favorites = []

    @classmethod
    def save_book(cls, data):
    
        query= '''
                INSERT INTO 
                books (title, num_of_pages)
                VALUES (%(title)s, %(num_of_pages)s);
        '''
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result


    @classmethod
    def get_all_books(cls):
        query = """SELECT * FROM books;"""
        books= []
        results = connectToMySQL(cls.DB).query_db(query)


        for all_books in results:
            books.append (cls(all_books))
        return books

    @classmethod
    def unfavorited_books(cls, data):
        query = """SELECT * FROM books
                WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id =  %(id)s); """
        
        results = connectToMySQL(cls.DB).query_db(query, data)

        books = []
        
        for row in results:
            books.append(cls(row))
        return books

    @classmethod
    def get_favorited_books(cls, data):
        query = """SELECT * FROM books
                WHERE books.id IN (SELECT book_id FROM favorites WHERE author_id =  %(id)s); """
        
        results = connectToMySQL(cls.DB).query_db(query, data)

        books = []
        
        for book in results:
            books.append(cls(book))
        return books

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)

        book = cls(results[0])

        for row in results:
            if row['authors.id'] == None:
                break
            data = {
                "id": row['authors.id'],
                "name": row['name'],
                "created_at": row['authors.created_at'],
                "updated_at": row['authors.updated_at']
            }
            book.authors_with_favorites.append(author_model.Authors(data))
        return book


# SELECT * FROM orders 
# JOIN items_orders ON orders.id = items_orders.order_id 
# JOIN items ON items.id = items_orders.item_id;




#     @classmethod
#     def get_all_shows(cls):
#         query= """
#             SELECT * FROM shows
#             JOIN Users
#             Where shows.user_id = users.id
#             ORDER BY shows.id DESC;
            
#         """
#         results = connectToMySQL(cls.DB).query_db(query)
#         print(results)
        
#         all_shows = []

#         for row in results:

#             one_show = cls(row)
            
#             user_data = {
#                 'id': row ['user_id'],
#                 'first_name': row ['first_name'],
#                 'last_name': row ['last_name'],
#                 'email': row ['email'],
#                 'password': row ['password'],
                
#                 'created_at': row ['created_at'],
#                 'updated_at': row ['updated_at']
#             }
#             one_show.creator = author_model.Users(user_data)
#             all_shows.append(one_show)
#         return all_shows

#     @classmethod
#     def get_one_show(cls, data):
#         query = """SELECT * FROM shows WHERE id = %(id)s;"""
#         results = connectToMySQL(cls.DB).query_db(query, data)
#         # return cls(results[0])
#         return cls(results[0])

#     @classmethod
#     def get_one_show_with_user(cls,data):
#         query='''
#             SELECT * FROM shows
#             JOIN users
#             ON shows.user_id = users.id
#             WHERE shows.id= %(id)s;

#         '''
#         results= connectToMySQL(cls.DB).query_db(query,data)
#         for row in results:
#             one_show = cls(row)
#             user_data={
#                     'id': row['users.id'],
#                     'first_name': row['first_name'],
#                     'last_name': row['last_name'],
#                     'email': row['email'],
#                     'password': ' ',
#                     'created_at': row['users.created_at'],
#                     'updated_at': row['users.updated_at']
#                 }
#             one_show.creator= author_model.Users(user_data)
#         return one_show

#     @classmethod
#     def update_show(cls,data):

#         query = """
#                 UPDATE shows
#                 SET 
#                 title = %(title)s,
#                 network = %(network)s, 
#                 description = %(description)s, 
#                 created_at = %(created_at)s
#                 WHERE id = %(id)s;
#         """
#                 #Semicolon not neeed, only best practice
#         result = connectToMySQL(cls.DB).query_db(query,data)
#         return result

#     @classmethod
#     def delete_show(cls, data):
#             query= '''
#                 DELETE FROM shows
#                 WHERE shows.id=%(id)s;
#             '''
#             return connectToMySQL(cls.DB).query_db(query, data)


#     @staticmethod
#     def validate_show(form_data):
#             is_valid = True
            
#             if len(form_data["title"]) < 3:
#                 flash("Title must not be blank.")
#                 is_valid = False
#             if len(form_data["network"]) < 3:
#                 flash("Network must not be blank.")
#                 is_valid = False
#             if form_data['created_at']  == '':
#                 flash("Date must not be blank.")
#                 is_valid = False
#             if len(form_data["description"]) < 3:
#                 flash("Description must not be blank.")
#                 is_valid = False

#             return is_valid