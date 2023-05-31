import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import mysql.connector

class SSISApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SSIS Application")
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.host_label = QLabel("Host:", self)
        self.host_label.setGeometry(20, 30, 100, 20)
        self.host_label.setFont(QFont("Arial", 12))

        self.host_input = QLineEdit(self)
        self.host_input.setGeometry(130, 30, 200, 30)
        self.host_input.setStyleSheet("background-color: white; font-size: 12px;")

        self.user_label = QLabel("User:", self)
        self.user_label.setGeometry(20, 80, 100, 20)
        self.user_label.setFont(QFont("Arial", 12))

        self.user_input = QLineEdit(self)
        self.user_input.setGeometry(130, 80, 200, 30)
        self.user_input.setStyleSheet("background-color: white; font-size: 12px;")

        self.password_label = QLabel("Password:", self)
        self.password_label.setGeometry(20, 130, 100, 20)
        self.password_label.setFont(QFont("Arial", 12))

        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(130, 130, 200, 30)
        self.password_input.setStyleSheet("background-color: white; font-size: 12px;")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.database_label = QLabel("Database:", self)
        self.database_label.setGeometry(20, 180, 100, 20)
        self.database_label.setFont(QFont("Arial", 12))

        self.database_input = QLineEdit(self)
        self.database_input.setGeometry(130, 180, 200, 30)
        self.database_input.setStyleSheet("background-color: white; font-size: 12px;")

        self.course_label = QLabel("Course Name:", self)
        self.course_label.setGeometry(20, 230, 100, 20)
        self.course_label.setFont(QFont("Arial", 12))

        self.course_input = QLineEdit(self)
        self.course_input.setGeometry(130, 230, 200, 30)
        self.course_input.setStyleSheet("background-color: white; font-size: 12px;")

        self.add_button = QPushButton("Add Course", self)
        self.add_button.setGeometry(130, 280, 200, 35)
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px;")
        self.add_button.clicked.connect(self.add_course)

    def add_course(self):
        host = self.host_input.text()
        user = self.user_input.text()
        password = self.password_input.text()
        database = self.database_input.text()
        course_name = self.course_input.text()

        try:
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if mydb.is_connected():
                print("Connected to the MySQL database")

                cursor = mydb.cursor()
                sql = "INSERT INTO courses (name) VALUES (%s)"
                values = (course_name,)
                cursor.execute(sql, values)
                mydb.commit()

                QMessageBox.information(self,"Success", "Course added successfully to the database.")
                mydb.close()
                
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", f"Error adding course: {err}")
                
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("macintosh")  # Apply the Fusion style
    ssis_app = SSISApplication()
    ssis_app.show()
    sys.exit(app.exec())