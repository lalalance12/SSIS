import csv
import sys
import os.path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog, QComboBox
from PyQt6.QtGui import QGuiApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("STUDENT INFORMATION SYSTEM")
        self.setGeometry(100, 100, 300, 400)
        
        self.student_fields = ['Name', 'ID', 'Course']
        self.course_fields = ['Name', 'Code']
        self.student_database = 'Students Information.csv'
        self.course_database = 'Course Information.csv'

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.v_layout = QVBoxLayout(self.central_widget)

        self.display_menu()

    def display_menu(self):
        self.menu_label = QLabel("Welcome to Student Information System", self)
        self.menu_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.v_layout.addWidget(self.menu_label)

        #A
        self.add_btn = QPushButton("Add Course", self)
        self.add_btn.clicked.connect(self.add_course)
        self.v_layout.addWidget(self.add_btn)
        
        #B
        self.add_btn = QPushButton("List of Course", self)
        self.add_btn.clicked.connect(self.list_course)
        self.v_layout.addWidget(self.add_btn)
        
        #C
        self.add_btn = QPushButton("Update Course", self)
        self.add_btn.clicked.connect(self.update_course)
        self.v_layout.addWidget(self.add_btn)
        
        #D
        self.add_btn = QPushButton("Delete Course", self)
        self.add_btn.clicked.connect(self.delete_course)
        self.v_layout.addWidget(self.add_btn)
        
   
        #1
        self.add_btn = QPushButton("Add Student", self)
        self.add_btn.clicked.connect(self.add_student)
        self.v_layout.addWidget(self.add_btn)

        #2
        self.search_id_btn = QPushButton("Search Student by ID", self)
        self.search_id_btn.clicked.connect(self.search_ID_student)
        self.v_layout.addWidget(self.search_id_btn)
        
        #3    
        self.search_name_btn = QPushButton("Search Student by Name", self)
        self.search_name_btn.clicked.connect(self.search_name_student)
        self.v_layout.addWidget(self.search_name_btn)

        #4 
        self.update_btn = QPushButton("Update Student", self)
        self.update_btn.clicked.connect(self.update_student)
        self.v_layout.addWidget(self.update_btn)
        
        #5 
        self.delete_btn = QPushButton("Delete Student", self)
        self.delete_btn.clicked.connect(self.delete_student)
        self.v_layout.addWidget(self.delete_btn)
    
        #6 
        self.list_btn = QPushButton("List Students", self)
        self.list_btn.clicked.connect(self.list_students)
        self.v_layout.addWidget(self.list_btn)
    
    # A
    def add_course(self):
        course_name, ok1 = QInputDialog.getText(self, 'Course Name', 'Enter course name:')
        course_code, ok2 = QInputDialog.getText(self, 'Course Code', 'Enter course code:')

        if ok1 and ok2:
            # Check if the course code already exists
            course_codes = []
            course_names = []
            if os.path.exists(self.course_database):
                with open(self.course_database, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    courses = list(reader)
                    course_codes = [row['Code'] for row in courses]
                    course_names = [row['Name'] for row in courses]
            else:
                with open(self.course_database, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['Name', 'Code'])

            if course_code in course_codes:
                QMessageBox.warning(self, "Error", "A course with the same code already exists!")
            elif course_name in course_names:
                QMessageBox.warning(self, "Error", "A course with the same name already exists!")
            elif not course_name or not course_code:
                QMessageBox.warning(self, "Error", "Course name and code cannot be blank!")
            else:
                with open(self.course_database, 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([course_name, course_code])
                QMessageBox.information(self, 'Success', 'Course added successfully!')
    # B
    def list_course(self):
        for i in reversed(range(self.v_layout.count())): 
            self.v_layout.itemAt(i).widget().setParent(None)

        table = QTableWidget(self.central_widget)
        table.setColumnCount(len(self.course_fields))
        table.setHorizontalHeaderLabels(self.course_fields)
        table.verticalHeader().setVisible(False)

        with open(self.course_database, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if set(reader.fieldnames) != set(self.course_fields):
                QMessageBox.warning(self, "Error", "The headers in the CSV file do not match the expected headers.")
                return
            data = [row for row in reader]

        table.setRowCount(len(data))
        for i, row_data in enumerate(data):
            for j, field in enumerate(self.course_fields):
                item = QTableWidgetItem(row_data[field])
                table.setItem(i, j, item)

        self.v_layout.addWidget(table)
        
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.display_menu)
        self.v_layout.addWidget(back_button)
        
        def remove_table():
            back_button.setParent(None)
            table.setParent(None)
        back_button.clicked.connect(remove_table)

    # C
    def update_course(self):
        with open(self.course_database, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            courses = [row[1] for row in reader]

        course_code, ok = QInputDialog.getItem(self, 'Update Course', 'Select course code:', courses)
        if ok:
            new_course_name, ok = QInputDialog.getText(self, 'Update Course', 'Enter new course name:')
            if ok:
                # Check for duplicates
                with open(self.course_database, 'r', newline='') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        if row['Name'] == new_course_name:
                            QMessageBox.warning(self, 'Error', 'The course name is already taken.')
                            return
            
                # Check for blank input
                if not new_course_name:
                    QMessageBox.warning(self, 'Error', 'Please enter a course name.')
                    return

                with open(self.course_database, 'r', newline='') as csv_file:
                    reader = csv.reader(csv_file)
                    rows = list(reader)
                with open(self.course_database, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for row in rows:
                        if row[1] == course_code:
                            row[0] = new_course_name
                        writer.writerow(row)
                QMessageBox.information(self, 'Success', 'Course updated successfully!')
 
    # D
    def delete_course(self):
        with open(self.course_database, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            courses = [row[1] for row in reader]

        course_code, ok = QInputDialog.getItem(self, 'Delete Course', 'Select course code:', courses)
        if ok:
            with open(self.course_database, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                rows = list(reader)
            with open(self.course_database, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for row in rows:
                    if row[1] != course_code:
                        writer.writerow(row)
            QMessageBox.information(self, 'Success', 'Course deleted successfully!')
    
    
    # 1    
    def add_student(self):
        self.add_widget = QWidget()
        self.add_layout = QVBoxLayout(self.add_widget)

        self.add_label = QLabel("Add Student Information", self.add_widget)
        self.add_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.add_layout.addWidget(self.add_label)

        self.input_widgets = []
        for field in self.student_fields:
            h_layout = QHBoxLayout()
            label = QLabel(field, self.add_widget)
            if field == 'Course':
                combo_box = QComboBox(self.add_widget)
                with open('Course Information.csv', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)
                    courses = [row[0] for row in reader]
                combo_box.addItems(courses)
                h_layout.addWidget(label)
                h_layout.addWidget(combo_box)
                self.input_widgets.append(combo_box)
            else:
                line_edit = QLineEdit(self.add_widget)
                h_layout.addWidget(label)
                h_layout.addWidget(line_edit)
                self.input_widgets.append(line_edit)
            self.add_layout.addLayout(h_layout)

        self.submit_btn = QPushButton("Submit", self.add_widget)
        self.submit_btn.clicked.connect(self.save_student)
        self.add_layout.addWidget(self.submit_btn)

        self.v_layout.addWidget(self.add_widget)

    # 1.A
    def save_student(self):
        student_data = []
        for widget in self.input_widgets:
            data = widget.currentText() if isinstance(widget, QComboBox) else widget.text()
            # Check for blank data
            if not data:
                QMessageBox.warning(self, "Error", "Please fill in all fields!")
                return
            student_data.append(data)
        
        header = ['Name', 'ID', 'Course']
        file_exists = os.path.isfile('Students Information.csv')

        if file_exists:
            # Check if student with same name or ID already exists
            with open('Students Information.csv', "r", encoding="utf-8", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Name'] == student_data[0] and row['ID'] == student_data[1]:
                        QMessageBox.warning(self, "Error", "A student with the same name and ID already exists!")
                        return
                    elif row['Name'] == student_data[0]:
                        QMessageBox.warning(self, "Error", "A student with the same name already exists!")
                        return
                    elif row['ID'] == student_data[1]:
                        QMessageBox.warning(self, "Error", "A student with the same ID already exists!")
                        return

        # Add new student to CSV file
        with open('Students Information.csv', "a", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header)
            writer.writerow(student_data)

        QMessageBox.information(self, "Success!", "Student information saved successfully")

        self.v_layout.removeWidget(self.add_widget)
        self.add_widget.deleteLater()
       
    # 2
    def search_ID_student(self):
        id = self.get_input('Enter ID to search')

        with open(self.student_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0:
                    if id == row[1]:
                        self.show_student_info(row)
                        break
            else:
                self.show_message_box('ID not found in our database')

    # 3
    def search_name_student(self):
        name = self.get_input('Enter name to search')

        with open(self.student_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0:
                    if name == row[0]:
                        self.show_student_info(row)
                        break
            else:
                self.show_message_box('Name not found in our database')
    
    # 3&4.A    
    def get_input(self, message):
        text, ok = QInputDialog.getText(self, 'Input Dialog', message)
        if ok:
            return text
    
    # 3&4.B 
    def show_student_info(self, student):
        info = f"Name: {student[0]}\nID: {student[1]}\nCourse: {student[2]}"
        self.show_message_box(info)

    # 3&4.C
    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Message")
        msg_box.setText(message)
        msg_box.exec()            


    # 4
    def update_student(self):
        id = self.get_input('Enter ID to update')

        with open(self.student_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            students = list(reader)

        found = False
        for i, student in enumerate(students):
            if len(student) > 0:
                if id == student[1]:
                    found = True
                    self.display_update_form(student, i)
                    break

        if not found:
            self.show_message_box('ID not found in our database')

    # 4.A
    def display_update_form(self, student, index):
        self.update_widget = QWidget(self)
        self.update_widget.setLayout(QVBoxLayout())

        self.input_widgets = []
        for field, value in zip(self.student_fields, student):
            h_layout = QHBoxLayout()
            label = QLabel(field, self.update_widget)

            if field == 'Course':
                combo_box = QComboBox(self.update_widget)
                with open('Course Information.csv', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)
                    courses = [row[0] for row in reader]
                combo_box.addItems(courses)
                combo_box.setCurrentText(value)
                h_layout.addWidget(label)
                h_layout.addWidget(combo_box)
                self.input_widgets.append(combo_box)
            else:
                line_edit = QLineEdit(self.update_widget)
                line_edit.setText(value)
                h_layout.addWidget(label)
                h_layout.addWidget(line_edit)
                self.input_widgets.append(line_edit)

            self.update_widget.layout().addLayout(h_layout)

        update_button = QPushButton("Update", self.update_widget)
        update_button.clicked.connect(lambda: self.update_student_data(index))
        self.update_widget.layout().addWidget(update_button)

        self.v_layout.addWidget(self.update_widget) 
    
    # 4.B
    def update_student_data(self, index):
        student_data = []
        for widget in self.input_widgets:
            if isinstance(widget, QComboBox):
                student_data.append(widget.currentText())
            else:
                student_data.append(widget.text())

        if any(not data for data in student_data):
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        with open('Students Information.csv', "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Name'] == student_data[0] and row['ID'] == student_data[1]:
                    QMessageBox.warning(self, "Error", "A student with the same name and ID already exists!")
                    return
                elif row['Name'] == student_data[0]:
                    QMessageBox.warning(self, "Error", "A student with the same name already exists!")
                    return
                elif row['ID'] == student_data[1]:
                    QMessageBox.warning(self, "Error", "A student with the same ID already exists!")
                    return

        with open('Students Information.csv', "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            students = list(reader)

        students[index] = student_data

        with open('Students Information.csv', "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(students)

        QMessageBox.information(self, "Success", "Data updated successfully")
        self.erase_update_form()
        
    # 4.C    
    def erase_update_form(self):
        if self.update_widget:
            self.v_layout.removeWidget(self.update_widget)
            self.update_widget.deleteLater()
            self.update_widget = None

    # 5
    def delete_student(self):
        ID = self.get_input('Enter ID of student to delete')
        name = {};
        
        with open(self.student_database, 'r') as f:
            students = list(csv.reader(f))

        found = False
        for i, student in enumerate(students):
            if len(student) > 0 and student[1] == ID:
                name = student[0]
                found = True
                break

        if found:
                students.pop(i)
                with open(self.student_database, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(students)
                self.show_message_box(f'( {name} | {ID} ) student information has been deleted successfully')
        else:
            self.show_message_box(f'Student with ID {ID} not found in the database')
    
    # 6        
    def list_students(self):
        for i in reversed(range(self.v_layout.count())): 
            self.v_layout.itemAt(i).widget().setParent(None)

        table = QTableWidget(self.central_widget)
        table.setColumnCount(len(self.student_fields))
        table.setHorizontalHeaderLabels(self.student_fields)
        table.verticalHeader().setVisible(False)

        with open(self.student_database, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if set(reader.fieldnames) != set(self.student_fields):
                QMessageBox.warning(self, "Error", "The headers in the CSV file do not match the expected headers.")
                return
            data = [row for row in reader]

        table.setRowCount(len(data))
        for i, row_data in enumerate(data):
            for j, field in enumerate(self.student_fields):
                item = QTableWidgetItem(row_data[field])
                table.setItem(i, j, item)

        self.v_layout.addWidget(table)
        
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.display_menu)
        self.v_layout.addWidget(back_button)
        
        def remove_table():
            back_button.setParent(None)
            table.setParent(None)
        back_button.clicked.connect(remove_table)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())