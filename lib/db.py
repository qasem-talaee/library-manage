import sqlite3
import datetime
import ast

class DB:
    
    def create_db(self):
        # Books table
        self.conn.execute('''
                          CREATE TABLE IF NOT EXISTS book
                          (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name CHAR(100) NOT NULL,
                            publisher CHAR(100) NOT NULL,
                            writer CHAR(100) NOT NULL,
                            subject CHAR(100) NOT NULL,
                            year CHAR(10) NOT NULL,
                            published CHAR(10) NOT NULL,
                            number CHAR(10) NOT NULL,
                            price CHAR(10) NOT NULL
                          );
                          ''')
        # Rent table
        self.conn.execute('''
                          CREATE TABLE IF NOT EXISTS rent
                          (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name CHAR(100) NOT NULL,
                            user_id CHAR(100) NOT NULL,
                            books CHAR(100) NOT NULL,
                            status CHAR(10) NOT NULL,
                            date DATE NOT NULL
                          );
                          ''')
        #Personal info table
        self.conn.execute('''
                          CREATE TABLE IF NOT EXISTS info
                          (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            shop_name CHAR(100) NOT NULL,
                            shop_add CHAR(200) NOT NULL,
                            shop_phone CHAR(100) NOT NULL,
                            name CHAR(100) NOT NULL,
                            email CHAR(10) NOT NULL
                          );
                          ''')
        # Sell table
        self.conn.execute('''
                          CREATE TABLE IF NOT EXISTS sell
                          (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            book_id CHAR(100) NOT NULL,
                            number CHAR(100) NOT NULL,
                            price CHAR(100) NOT NULL,
                            user_id CHAR(100) NOT NULL,
                            user_name CHAR(100) NOT NULL
                          );
                          ''')
    
    def __init__(self):
        self.conn = sqlite3.connect('libdb.db')
        self.create_db()
    
    def search_rent(self, user_id):
        cursor = self.conn.execute("SELECT * FROM rent WHERE user_id='{user_id}' AND status='0';".format(user_id=user_id))
        out = []
        for row in cursor:
            rent = []
            for item in row:
                rent.append(item)
            out.append(rent)
        return out
    
    def change_rent_status(self, id):
        self.conn.execute("UPDATE rent SET status='1' WHERE id={id};".format(id=id))
    
    def get_rent_cart(self, id):
        cursor = self.conn.execute("SELECT books FROM rent WHERE id={id}".format(id=id))
        for row in cursor:
            return ast.literal_eval(row[0])
    
    def get_all_rent(self):
        cursor = self.conn.execute("SELECT * FROM rent WHERE status='0';")
        out = []
        for row in cursor:
            rent = []
            for item in row:
                rent.append(item)
            out.append(rent)
        return out
    
    def rent_book(self, id, name, cart):
        db_string = "INSERT INTO rent (name, user_id, books, status, date) VALUES (?,?,?,?,?);"
        data = (name, id, str(cart), '0', str(datetime.datetime.now()))
        cursor = self.conn.cursor()
        cursor.execute(db_string, data)
        self.conn.commit()
        cursor.close()
    
    def sell_book(self, id, name, cart):
        for i in range(len(cart)):
            db_string = "INSERT INTO sell (book_id, number, price, user_id, user_name) VALUES (?,?,?,?,?);"
            data = (cart[i]['id'], cart[i]['number'], cart[i]['price'], id, name)
            curser = self.conn.cursor()
            curser.execute(db_string, data)
            self.conn.commit()
            curser.close()
       
    def add_book(self, name, publisher, writer, subject, year, published, number, price):
        db_string = "INSERT INTO book (name, publisher, writer, subject, year, published, number, price) VALUES (?,?,?,?,?,?,?,?);"
        data = (name, publisher, writer, subject, year, published, number, price)
        curser = self.conn.cursor()
        curser.execute(db_string, data)
        self.conn.commit()
        curser.close()
    
    def edit_book(self, id, name, publisher, writer, subject, year, published, number, price):
        db_string = "UPDATE book SET name=?, publisher=?, writer=?, subject=?, year=?, published=?, number=?, price=? WHERE id=?;"
        data = (name, publisher, writer, subject, year,published, number, price, id)
        cursor = self.conn.cursor()
        cursor.execute(db_string, data)
        self.conn.commit()
        cursor.close()
    
    def del_book(self, id):
        cursor = self.conn.execute("DELETE FROM book WHERE id={id};".format(id=id))
        cursor.close()
        
    def count_book(self):
        cursor = self.conn.execute('SELECT Count(*) FROM book;')
        number = 0
        for row in cursor:
            number = row[0]
        cursor.close()
        return int(number)
      
    def select_all_book(self):
        cursor = self.conn.execute('SELECT * FROM book')
        out = []
        for row in cursor:
            book = []
            book.append(row[0])
            book.append(row[1])
            book.append(row[2])
            book.append(row[3])
            book.append(row[4])
            book.append(row[5])
            book.append(row[6])
            book.append(row[7])
            book.append(row[8])
            out.append(book)
        cursor.close()
        return out
    
    def search_book(self, werb):
        werb = werb.rstrip().lstrip().split(' ')
        like = '%'
        for i in range(len(werb)):
            like += '{w}%'.format(w=werb[i])
        cursor = self.conn.execute("SELECT * FROM book WHERE name LIKE '{like}';".format(like=like))
        out = []
        for row in cursor:
            book = []
            book.append(row[0])
            book.append(row[1])
            book.append(row[2])
            book.append(row[3])
            book.append(row[4])
            book.append(row[5])
            book.append(row[6])
            book.append(row[7])
            book.append(row[8])
            out.append(book)
        cursor.close()
        return out
      
    def select_by_id(self, id):
        cursor = self.conn.execute('SELECT * FROM book WHERE id={id};'.format(id=id))
        out = []
        for row in cursor:
            book = []
            book.append(row[0])
            book.append(row[1])
            book.append(row[2])
            book.append(row[3])
            book.append(row[4])
            book.append(row[5])
            book.append(row[6])
            book.append(row[7])
            book.append(row[8])
            out.append(book)
        cursor.close()
        return out