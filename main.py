from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QHeaderView, QTableWidgetItem
import sys
from datetime import datetime

from ui import res
from lib import db

class LibManage(QMainWindow):
    
    def buttons_menu(self):
        def set_index_tab(index):
            self.tabWidget.setCurrentIndex(index)
        self.listButton.clicked.connect(lambda *args : set_index_tab(0))
        self.sellButton.clicked.connect(lambda *args : set_index_tab(1))
        self.histButton.clicked.connect(lambda *args : set_index_tab(2))
        self.addpageButton.clicked.connect(lambda *args : set_index_tab(3))
        self.editpageButton.clicked.connect(lambda *args : set_index_tab(4))
    
    def __init__(self):
        super(LibManage, self).__init__()
        uic.loadUi('ui/lib.ui', self)
        self.db = db.DB()
        self.tabWidget.setCurrentIndex(0)
        self.buttons_menu()
        self.actionAbout_Me.triggered.connect(self.about_me)
        self.pushButton_8.clicked.connect(self.add_book)
        self.tabWidget.currentChanged.connect(self.change_tab)
        self.pushButton_7.clicked.connect(self.search_book)
        self.pushButton_9.clicked.connect(self.refresh_book)
        self.pushButton_16.clicked.connect(self.search_edit)
        self.pushButton_17.clicked.connect(self.refresh_edit)
        self.pushButton_18.clicked.connect(self.add_to_edit)
        self.pushButton_20.clicked.connect(self.edit_book_bot)
        self.pushButton_19.clicked.connect(self.remove_book)
        self.pushButton_14.clicked.connect(self.add_to_cart)
        self.pushButton_10.clicked.connect(self.search_cart)
        self.pushButton_11.clicked.connect(self.refresh_cart)
        self.pushButton_15.clicked.connect(self.empty_cart)
        self.pushButton_12.clicked.connect(self.sell_cart)
        self.pushButton_13.clicked.connect(self.rent_cart)
        self.pushButton_24.clicked.connect(self.add_change_rent)
        self.pushButton_25.clicked.connect(self.change_rent)
        self.pushButton_22.clicked.connect(self.search_rent)
        self.pushButton_23.clicked.connect(self.refresh_rent)
        self.book_id_edit = None
        self.rent_id_change = None
        self.cart = []
        self.change_tab(0)
        self.show()
    
    def refresh_rent(self):
        self.change_tab(2)
        self.lineEdit_17.setText('')
    
    def search_rent(self):
        user_input = self.lineEdit_17.text()
        if user_input != '':
            rents = self.db.search_rent(user_input)
            if len(rents) == 0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("No Rent found.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                rowCount = len(rents)
                self.tableWidget.setColumnCount(5)
                self.tableWidget.setRowCount(rowCount)
                self.tableWidget.setHorizontalHeaderLabels(['Id', 'Name', 'User Id', 'Date', 'Days Gone By'])
                if len(rents) != 0:
                    for i in range(len(rents)):
                        for j in range(5):
                            if j == 4:
                                date_format = '%Y-%m-%d %H:%M:%S.%f'
                                a = datetime.strptime(rents[i][j+1], date_format)
                                b = datetime.strptime(str(datetime.now()), date_format)
                                delta = b - a
                                self.tableWidget.setItem(i, j, QTableWidgetItem(str(delta.days)))
                            if j == 3:
                                self.tableWidget.setItem(i, j, QTableWidgetItem(rents[i][j+2]))
                            else:
                                self.tableWidget.setItem(i, j, QTableWidgetItem(str(rents[i][j])))
                #Table will fit the screen horizontally
                self.tableWidget.horizontalHeader().setStretchLastSection(True)
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def change_rent(self):
        if self.rent_id_change == None:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please select a book from above table.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Change the status of the borrowed book")
            msg.setText("Are you sure you want to do this?")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.setIcon(QMessageBox.Icon.Information)
            result = msg.exec_()
            if result ==  QMessageBox.StandardButton.Ok:
                self.db.change_rent_status(self.rent_id_change)
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Status changed successfully.")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.exec_()
                self.rent_id_change = None
                self.tableWidget_6.setColumnCount(2)
                self.tableWidget_6.setRowCount(0)
                self.tableWidget_6.setHorizontalHeaderLabels(['Name', 'Number'])
                #Table will fit the screen horizontally
                self.tableWidget_6.horizontalHeader().setStretchLastSection(True)
                self.tableWidget_6.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.change_tab(2)
    
    def add_change_rent(self):
        try:
            user_input_id = self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please select a book from above table.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            self.rent_id_change = user_input_id
            rents = self.db.get_rent_cart(self.rent_id_change)
            rowCount = len(rents)
            self.tableWidget_6.setColumnCount(2)
            self.tableWidget_6.setRowCount(rowCount)
            self.tableWidget_6.setHorizontalHeaderLabels(['Name', 'Number'])
            for i in range(rowCount):
                for j in range(2):
                    if j == 0:
                        self.tableWidget_6.setItem(i, j, QTableWidgetItem(str(rents[i]['name'])))
                    if j == 1:
                        self.tableWidget_6.setItem(i, j, QTableWidgetItem(str(rents[i]['number'])))
            #Table will fit the screen horizontally
            self.tableWidget_6.horizontalHeader().setStretchLastSection(True)
            self.tableWidget_6.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def rent_cart(self):
        user_id = self.lineEdit_5.text()
        user_name = self.lineEdit_7.text()
        if user_id == '' or user_name == '' or self.cart == []:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Enter Information")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Lend Cart")
            msg.setText("Are you sure you want to do this?")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.setIcon(QMessageBox.Icon.Information)
            result = msg.exec_()
            if result ==  QMessageBox.StandardButton.Ok:
                self.db.rent_book(user_id, user_name, self.cart)
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Cart Lended.")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.exec_()
                self.lineEdit_6.setText('')
                self.change_tab(1)
                self.cart = []
                self.tableWidget_5.setColumnCount(4)
                self.tableWidget_5.setRowCount(len(self.cart))
                self.tableWidget_5.setHorizontalHeaderLabels(['Name', 'Price', 'Number', 'T-Price'])
                self.label_11.setText('')
    
    def sell_cart(self):
        user_id = self.lineEdit_5.text()
        user_name = self.lineEdit_7.text()
        if user_id == '' or user_name == '' or self.cart == []:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Enter Information")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Sell Cart")
            msg.setText("Are you sure you want to do this?")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.setIcon(QMessageBox.Icon.Information)
            result = msg.exec_()
            if result ==  QMessageBox.StandardButton.Ok:
                self.db.sell_book(user_id, user_name, self.cart)
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Cart Selled.")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.exec_()
                self.lineEdit_6.setText('')
                self.change_tab(1)
                self.cart = []
                self.tableWidget_5.setColumnCount(4)
                self.tableWidget_5.setRowCount(len(self.cart))
                self.tableWidget_5.setHorizontalHeaderLabels(['Name', 'Price', 'Number', 'T-Price'])
                self.label_11.setText('')
    
    def empty_cart(self):
        msg = QMessageBox()
        msg.setWindowTitle("Empty Cart")
        msg.setText("Are you sure you want to do this?")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg.setIcon(QMessageBox.Icon.Warning)
        result = msg.exec_()
        if result ==  QMessageBox.StandardButton.Ok:
            self.cart = []
            self.tableWidget_5.setColumnCount(4)
            self.tableWidget_5.setRowCount(len(self.cart))
            self.tableWidget_5.setHorizontalHeaderLabels(['Name', 'Price', 'Number', 'T-Price'])
            self.label_11.setText('')
    
    def refresh_cart(self):
        self.lineEdit_6.setText('')
        self.change_tab(1)
    
    def search_cart(self):
        user_input = self.lineEdit_6.text()
        if user_input != '':
            books = self.db.search_book(user_input)
            if len(books) == 0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("No book found.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                rowCount = len(books)
                self.tableWidget_3.setColumnCount(3)
                self.tableWidget_3.setRowCount(rowCount)
                self.tableWidget_3.setHorizontalHeaderLabels(['Id', 'Name', 'Writer'])
                if len(books) != 0:
                    for i in range(len(books)):
                        for j in range(3):
                            if j == 2:
                                self.tableWidget_3.setItem(i, j, QTableWidgetItem(books[i][j+1]))
                            else:
                                self.tableWidget_3.setItem(i, j, QTableWidgetItem(str(books[i][j])))
    
    def add_to_cart(self):
        try:
            user_input_id = self.tableWidget_4.item(self.tableWidget_4.currentRow(),0).text()
            user_input_name = self.tableWidget_4.item(self.tableWidget_4.currentRow(),1).text()
            user_input_price = self.tableWidget_4.item(self.tableWidget_4.currentRow(),4).text()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please select a book from above table.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            number = self.spinBox_3.text()
            self.cart.append({
                'id': user_input_id,
                'name': user_input_name,
                'price': user_input_price,
                'number': number,
            })
            self.tableWidget_5.setColumnCount(4)
            self.tableWidget_5.setRowCount(len(self.cart))
            self.tableWidget_5.setHorizontalHeaderLabels(['Name', 'Price', 'Number', 'T-Price'])
            if len(self.cart) != 0:
                for i in range(len(self.cart)):
                    self.tableWidget_5.setItem(i, 0, QTableWidgetItem(str(self.cart[i]['name'])))
                    self.tableWidget_5.setItem(i, 1, QTableWidgetItem(str(self.cart[i]['price'])))
                    self.tableWidget_5.setItem(i, 2, QTableWidgetItem(str(self.cart[i]['number'])))
                    t_price = int(self.cart[i]['number']) * float(self.cart[i]['price'])
                    self.tableWidget_5.setItem(i, 3, QTableWidgetItem(str(t_price)))
            # cal total
            total = 0
            for i in range(len(self.cart)):
                total += int(self.cart[i]['number']) * float(self.cart[i]['price'])
            self.label_11.setText(str(total))
    
    def remove_book(self):
        if self.book_id_edit == None:
            pass
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Delete Book")
            msg.setText("Are you sure you want to do this?")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msg.setIcon(QMessageBox.Icon.Warning)
            result = msg.exec_()
            if result ==  QMessageBox.StandardButton.Ok:
                self.db.del_book(self.book_id_edit)
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Book deleted successfully.")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.exec_()
                self.book_id_edit = None
                self.lineEdit_9.setText('')
                self.lineEdit_11.setText('')
                self.lineEdit_10.setText('')
    
    def edit_book_bot(self):
        if self.book_id_edit == None:
            pass
        else:
            name = self.lineEdit_9.text()
            publisher = self.lineEdit_11.text()
            writer = self.lineEdit_10.text()
            subject = self.comboBox_2.currentText()
            year = self.spinBox_6.text()
            published = self.spinBox_4.text()
            number = self.spinBox_5.text()
            price = self.doubleSpinBox_2.text()
            self.db.edit_book(self.book_id_edit, name, publisher, writer, subject, year, published, number, price)
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Book edited successfully.")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec_()
            self.book_id_edit = None
            self.lineEdit_9.setText('')
            self.lineEdit_11.setText('')
            self.lineEdit_10.setText('')
    
    def refresh_edit(self):
        self.change_tab(4)
    
    def add_to_edit(self):
        try:
            user_input = self.tableWidget_3.item(self.tableWidget_3.currentRow(),0).text()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Please select a book from above table.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            book = self.db.select_by_id(user_input)
            self.book_id_edit = book[0][0]
            self.lineEdit_9.setText(book[0][1])
            self.lineEdit_11.setText(book[0][2])
            self.lineEdit_10.setText(book[0][3])
            self.comboBox_2.setCurrentIndex(self.comboBox_2.findText(book[0][4], QtCore.Qt.MatchFixedString))
            self.spinBox_6.setValue(int(book[0][5]))
            self.spinBox_4.setValue(int(book[0][6]))
            self.spinBox_5.setValue(int(book[0][7]))
            self.doubleSpinBox_2.setValue(float(book[0][8]))
            
    def search_edit(self):
        user_input = self.lineEdit_8.text()
        if user_input != '':
            books = self.db.search_book(user_input)
            if len(books) == 0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("No book found.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                rowCount = len(books)
                self.tableWidget_4.setColumnCount(5)
                self.tableWidget_4.setRowCount(rowCount)
                self.tableWidget_4.setHorizontalHeaderLabels(['Id', 'Name', 'Publisher', 'Writer', 'Price'])
                if len(books) != 0:
                    for i in range(len(books)):
                        for j in range(5):
                            if j == 4:
                                self.tableWidget_4.setItem(i, j, QTableWidgetItem(str(books[i][j+4])))
                            else:
                                self.tableWidget_4.setItem(i, j, QTableWidgetItem(str(books[i][j])))
                #Table will fit the screen horizontally
                self.tableWidget_4.horizontalHeader().setStretchLastSection(True)
                self.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def refresh_book(self):
        self.lineEdit.setText('')
        #print(self.tableWidget_2.item(self.tableWidget_2.currentRow(),0).text())
        self.change_tab(0)
    
    def search_book(self):
        user_input = self.lineEdit.text()
        if user_input != '':
            books = self.db.search_book(user_input)
            if len(books) == 0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("No book found.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec_()
            else:
                rowCount = len(books)
                self.tableWidget_2.setColumnCount(8)
                self.tableWidget_2.setRowCount(rowCount)
                self.tableWidget_2.setHorizontalHeaderLabels(['Name', 'Publisher', 'Writer', 'Subject', 'Year', 'Published', 'Number', 'Price'])
                for i in range(len(books)):
                    for j in range(8):
                        self.tableWidget_2.setItem(i, j, QTableWidgetItem(books[i][j+1]))
                #Table will fit the screen horizontally
                self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
                self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def change_tab(self, index):
        if index == 0:
            rowCount = self.db.count_book()
            books = self.db.select_all_book()
            self.tableWidget_2.setColumnCount(8)
            self.tableWidget_2.setRowCount(rowCount)
            self.tableWidget_2.setHorizontalHeaderLabels(['Name', 'Publisher', 'Writer', 'Subject', 'Year', 'Published', 'Number', 'Price'])
            if len(books) != 0:
                for i in range(len(books)):
                    for j in range(8):
                        self.tableWidget_2.setItem(i, j, QTableWidgetItem(books[i][j+1]))
            #Table will fit the screen horizontally
            self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
            self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if index == 1:
            rowCount = self.db.count_book()
            books = self.db.select_all_book()
            self.tableWidget_4.setColumnCount(5)
            self.tableWidget_4.setRowCount(rowCount)
            self.tableWidget_4.setHorizontalHeaderLabels(['Id', 'Name', 'Publisher', 'Writer', 'Price'])
            if len(books) != 0:
                for i in range(len(books)):
                    for j in range(5):
                        if j == 4:
                            self.tableWidget_4.setItem(i, j, QTableWidgetItem(str(books[i][j+4])))
                        else:
                            self.tableWidget_4.setItem(i, j, QTableWidgetItem(str(books[i][j])))
            #Table will fit the screen horizontally
            self.tableWidget_4.horizontalHeader().setStretchLastSection(True)
            self.tableWidget_4.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if index == 2:
            rents = self.db.get_all_rent()
            rowCount = len(rents)
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setRowCount(rowCount)
            self.tableWidget.setHorizontalHeaderLabels(['Id', 'Name', 'User Id', 'Date', 'Days Gone By'])
            if len(rents) != 0:
                for i in range(len(rents)):
                    for j in range(5):
                        if j == 4:
                            date_format = '%Y-%m-%d %H:%M:%S.%f'
                            a = datetime.strptime(rents[i][j+1], date_format)
                            b = datetime.strptime(str(datetime.now()), date_format)
                            delta = b - a
                            self.tableWidget.setItem(i, j, QTableWidgetItem(str(delta.days)))
                        if j == 3:
                            self.tableWidget.setItem(i, j, QTableWidgetItem(rents[i][j+2]))
                        else:
                            self.tableWidget.setItem(i, j, QTableWidgetItem(str(rents[i][j])))
            #Table will fit the screen horizontally
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if index == 4:
            rowCount = self.db.count_book()
            books = self.db.select_all_book()
            self.tableWidget_3.setColumnCount(3)
            self.tableWidget_3.setRowCount(rowCount)
            self.tableWidget_3.setHorizontalHeaderLabels(['Id', 'Name', 'Writer'])
            if len(books) != 0:
                for i in range(len(books)):
                    for j in range(3):
                        if j == 2:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem(books[i][j+1]))
                        else:
                            self.tableWidget_3.setItem(i, j, QTableWidgetItem(str(books[i][j])))
            #Table will fit the screen horizontally
            self.tableWidget_3.horizontalHeader().setStretchLastSection(True)
            self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def add_book(self):
        name = self.lineEdit_2.text()
        publiser = self.lineEdit_3.text()
        writer = self.lineEdit_4.text()
        subject = self.comboBox.currentText()
        year = self.dateEdit.text()
        published = str(self.spinBox.text())
        number = str(self.spinBox_2.text())
        price = str(self.doubleSpinBox.text())
        if name == '' or publiser == '' or writer == '':
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("You must set information.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec_()
        else:
            self.db.add_book(name, publiser, writer, subject, year, published, number, price)
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Book added successfully.")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec_()
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
    
    def about_me(self):
        msg = QMessageBox()
        msg.setWindowTitle("About Me")
        msg.setTextFormat(QtCore.Qt.TextFormat.RichText)
        msg.setText("Hi. I am Qasem Talaee.<br>"
                    "I am a computer programmer.<br>"
                    "I wrote this software for free, hoping that you will be successful.<br>"
                    "<b><i>Enjoy It My Friend !</i></b><br><br>"
                    "My Github : <a href='https://github.com/qasem-talaee'>https://github.com/qasem-talaee</a><br>"
                    "My Website : <a href='http://qtle.ir'>http://qtle.ir</a><br>"
                    "My Email : <a href='mailto:qasem.talaee1375@gmail.com'>qasem.talaee1375@gmail.com</a><br>")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec_()
        

app = QApplication(sys.argv)
window = LibManage()
app.exec_()