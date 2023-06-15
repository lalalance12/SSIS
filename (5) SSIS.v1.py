import csv
import sys
import os.path
from PyQt6.QtWidgets import QApplication, QAbstractScrollArea, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog, QComboBox, QDialog
from PyQt6.QtCore import Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSIS")
        self.setGeometry(100, 100, 300, 400)
        
        self.student_fields = ['Name', 'ID', 'Course Code']
        self.course_fields = ['Name', 'Code']
        self.student_database = 'Students Information.csv'
        self.course_database = 'Course Information.csv'

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.v_layout = QVBoxLayout(self.central_widget)

        self.display_menu()

    def display_menu(self):
        
        title_label = QLabel("Simple Student Information System")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "color: rgb(255, 255, 255);"  # Text color (white)
            "background-color: rgb(0, 0, 100);"  # Background color (indigo)
            "font-size: 30px;"  # Font size
            "font-weight: bold;"  # Font weight (bold)
            "font-family: 'Arial', sans-serif;"  # Font family
        )

        # First column
        column1_layout = QVBoxLayout()
        self.add_btn = QPushButton("Add Course", self)
        self.add_btn.clicked.connect(self.add_course)
        column1_layout.addWidget(self.add_btn)
        
        self.list_btn = QPushButton("List of Course", self)
        self.list_btn.clicked.connect(self.list_course)
        column1_layout.addWidget(self.list_btn)
        
        self.update_btn = QPushButton("Update Course", self)
        self.update_btn.clicked.connect(self.update_course)
        column1_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("Delete Course", self)
        self.delete_btn.clicked.connect(self.delete_course)
        column1_layout.addWidget(self.delete_btn)
        
        # Second column
        column2_layout = QVBoxLayout()
        self.add_student_btn = QPushButton("Add Student", self)
        self.add_student_btn.clicked.connect(self.add_student)
        column2_layout.addWidget(self.add_student_btn)
        
        self.add_student_btn.clicked.connect(self.disable_add_student_button) 

        self.search_id_btn = QPushButton("Search Student by ID", self)
        self.search_id_btn.clicked.connect(self.search_ID_student)
        column2_layout.addWidget(self.search_id_btn)
        
        self.search_name_btn = QPushButton("Search Student by Name", self)
        self.search_name_btn.clicked.connect(self.search_name_student)
        column2_layout.addWidget(self.search_name_btn)

        self.update_student_btn = QPushButton("Update Student", self)
        self.update_student_btn.clicked.connect(self.update_student)
        column2_layout.addWidget(self.update_student_btn)
        
        self.delete_student_btn = QPushButton("Delete Student", self)
        self.delete_student_btn.clicked.connect(self.delete_student)
        column2_layout.addWidget(self.delete_student_btn)
    
        self.list_student_btn = QPushButton("List Students", self)
        self.list_student_btn.clicked.connect(self.list_students)
        column2_layout.addWidget(self.list_student_btn)
        
        # Add both columns to the main layout
        main_layout = QVBoxLayout()
        sub_layout = QHBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addLayout(sub_layout)
        sub_layout.addLayout(column1_layout)
        sub_layout.addLayout(column2_layout)
        
        self.v_layout.addLayout(main_layout)
        
    #0.1
    def disable_add_student_button(self):
        self.add_student_btn.setEnabled(False)
    #0.2
    def enable_add_student_button(self):
        self.add_student_btn.setEnabled(True)
    
    # A
    def add_course(self):
        course_name, ok1 = QInputDialog.getText(self, 'Course Name', 'Enter course name:')
        if not ok1:
            return

        course_code, ok2 = QInputDialog.getText(self, 'Course Code', 'Enter course code:')

        if ok2:
            # Check if the course code already exists
            course_codes = []
            course_names = []
            if os.path.exists(self.course_database):
                with open(self.course_database, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    courses = list(reader)
                    course_codes = [row['Code'] for row in courses]
                    course_names = [row['Name'] for row in courses]

            if course_code in course_codes:
                QMessageBox.warning(self, "Error", "A course with the same code already exists!")
            elif course_name in course_names:
                QMessageBox.warning(self, "Error", "A course with the same name already exists!")
            elif not course_code:
                QMessageBox.warning(self, "Error", "Course code cannot be blank!")
            else:
                self.add_student_btn.setEnabled(True)
                if not os.path.exists(self.course_database):
                    with open(self.course_database, 'w', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(['Name', 'Code'])

                with open(self.course_database, 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([course_name, course_code])
                QMessageBox.information(self, 'Success', 'Course added successfully!')
        else:
            return
                
    # B
    def list_course(self):
        # Check if the CSV file exists
        if not os.path.exists(self.course_database):
            QMessageBox.warning(self, "Error", "No course has been added yet.")
            return

        
        with open(self.course_database, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            
            # Check if there are any rows excluding the header
            if len(list(reader)) <= 1:
                QMessageBox.warning(self, "Error", "No course has been added yet.")
                return
            
            
        # Create a dialog window to display the list of courses
        dialog = QDialog(self)
        dialog.setWindowTitle("List of Courses")
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.resize(400, 300)
        layout = QVBoxLayout(dialog)

        table = QTableWidget(dialog)
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
                item.setFlags(item.flags() & Qt.ItemFlag.ItemIsEditable)  # Set cell as read-only
                table.setItem(i, j, item)

        table.resizeColumnsToContents()  # Adjust column widths
        table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)  # Adjust cell sizes to content

        layout.addWidget(table)
        dialog.exec()  # Display the dialog window

    # C
    def update_course(self):
        # Check if the CSV file exists
        if not os.path.exists(self.course_database):
            QMessageBox.warning(self, "Error", "No course has been added yet.")
            return
        
        with open(self.course_database, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            
            # Check if there are any rows excluding the header
            if len(list(reader)) <= 1:
                QMessageBox.warning(self, "Error", "No course has been added yet.")
                return
            csv_file.seek(0)  # Reset file pointer to the beginning
            
            
            next(reader)
            courses = [row[1] for row in reader]

        course_code, ok = QInputDialog.getItem(self, 'Update Course', 'Select course code:', courses)
        if ok:
            options = ['Course Name', 'Course Code']
            choice, ok = QInputDialog.getItem(self, 'Update Course', 'Select option:', options)
            if ok:
                if choice == 'Course Name':
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
                        QMessageBox.information(self, 'Success', 'Course name updated successfully!')

                elif choice == 'Course Code':
                    new_course_code, ok = QInputDialog.getText(self, 'Update Course', 'Enter new course code:')
                    if ok:
                        # Check for duplicates
                        with open(self.course_database, 'r', newline='') as csv_file:
                            reader = csv.DictReader(csv_file)
                            for row in reader:
                                if row['Code'] == new_course_code:
                                    QMessageBox.warning(self, 'Error', 'The course code is already taken.')
                                    return

                        # Check for blank input
                        if not new_course_code:
                            QMessageBox.warning(self, 'Error', 'Please enter a course code.')
                            return

                        with open(self.course_database, 'r', newline='') as csv_file:
                            reader = csv.reader(csv_file)
                            rows = list(reader)
                        with open(self.course_database, 'w', newline='') as csv_file:
                            writer = csv.writer(csv_file)
                            for row in rows:
                                if row[1] == course_code:
                                    row[1] = new_course_code
                                writer.writerow(row)
                        QMessageBox.information(self, 'Success', 'Course code updated successfully!')
                                           
    # D
    def delete_course(self):
        # Check if the CSV file exists
        if not os.path.exists(self.course_database):
            QMessageBox.warning(self, "Error", "No course has been added yet.")
            return

        with open(self.course_database, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            # Check if there are any rows excluding the header
            if len(list(reader)) <= 1:
                QMessageBox.warning(self, "Error", "No course has been added yet.")
                return
            csv_file.seek(0)  # Reset file pointer to the beginning

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
        
        if not os.path.exists('Course Information.csv'):
            QMessageBox.warning(self, "Error", "No courses added yet!")
            return
        
        with open(self.course_database, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            # Check if there are any rows excluding the header
            if len(list(reader)) <= 1:
                QMessageBox.warning(self, "Error", "No course has been added yet.")
                return
        
        
        self.add_widget = QWidget()
        self.add_layout = QVBoxLayout(self.add_widget)

        self.add_label = QLabel("Add Student Information", self.add_widget)
        self.add_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.add_layout.addWidget(self.add_label)

        self.input_widgets = []
        for field in self.student_fields:
            h_layout = QHBoxLayout()
            label = QLabel(field, self.add_widget)
            if field == 'Course Code':
                combo_box = QComboBox(self.add_widget)
                with open('Course Information.csv', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)
                    courses = [row[1] for row in reader]
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
        
        self.back_btn = QPushButton("Back", self.add_widget)
        self.back_btn.clicked.connect(self.delete_form)
        self.add_layout.addWidget(self.back_btn)
        
        self.enable_add_student_button()
        self.update_student_btn.setEnabled(True)

        self.v_layout.addWidget(self.add_widget)
        
    # 1.A    
    def delete_form(self):
        self.v_layout.removeWidget(self.add_widget)
        self.add_widget.deleteLater()
        self.enable_add_student_button()   
         
    # 1.B
    def save_student(self):
        student_data = []
        for widget in self.input_widgets:
            data = widget.currentText() if isinstance(widget, QComboBox) else widget.text()
            # Check for blank data
            if not data:
                QMessageBox.warning(self, "Error", "Please fill in all fields!")
                return
            student_data.append(data)
            
        
        header = ['Name', 'ID', 'Course Code']
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
        self.enable_add_student_button()

        self.v_layout.removeWidget(self.add_widget)
        self.add_widget.deleteLater()
       
    # 2
    def search_ID_student(self):
        # Check if the CSV file exists
        if not os.path.exists(self.student_database):
            QMessageBox.warning(self, "Error", "No student has been added yet.")
            return
        
        # Check if there are data in the CSV file except the header
        with open(self.student_database, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            
            # Check if there are any rows excluding the header
            if len(list(reader)) <= 1:
                QMessageBox.warning(self, "Error", "No course has been added yet.")
                return
            
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
        # Check if the CSV file exists
        if not os.path.exists(self.student_database):
            QMessageBox.warning(self, "Error", "No student has been added yet.")
            return
        
        # Check if there are data in the CSV file except the header
        with open(self.student_database, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            
            # Check if there are any rows excluding the header
            if len(list(reader)) <= 1:
                QMessageBox.warning(self, "Error", "No course has been added yet.")
                return
            
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
        info = f"Name: {student[0]}\nID: {student[1]}\nCourse Code: {student[2]}"
        self.show_message_box(info)

    # 3&4.C
    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Message")
        msg_box.setText(message)
        msg_box.exec()            

    # 4
    def update_student(self):
        # Check if the CSV file exists
        if not os.path.exists(self.student_database):
            QMessageBox.warning(self, "Error", "No student has been added yet.")
            return
        
        # Check if there are data in the CSV file except the header
        with open(self.student_database, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            
            # Check if there are any rows excluding the header
            if len(list(reader)) <= 1:
                QMessageBox.warning(self, "Error", "No course has been added yet.")
                return
            
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
                    self.update_student_btn.setEnabled(False)
                    self.add_student_btn.setEnabled(False)
                    self.delete_student_btn.setEnabled(False)
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

            if field == 'Course Code':
                combo_box = QComboBox(self.update_widget)
                with open('Course Information.csv', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)
                    courses = [row[1] for row in reader]
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
        
        back_button = QPushButton("Back", self.update_widget)
        back_button.clicked.connect(self.erase_update_form)
        self.update_widget.layout().addWidget(back_button)

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
                if row['ID'] != student_data[1] and row['Name'] != student_data[0]:
                    if row['Name'] == student_data[0] and row['ID'] == student_data[1]:
                        QMessageBox.warning(self, "Error", "A student with the same name and ID already exists!")
                        return
                    elif row['Name'] == student_data[0]:
                        QMessageBox.warning(self, "Error", "A student with the same name already exists!")
                        return
                    elif row['ID'] == student_data[1]:
                        QMessageBox.warning(self, "Error", "A student with the same ID already exists!")
                        return
                    elif row['ID'] == student_data[1] and row['Name'] == student_data[0]:
                        continue
    

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
            
            self.update_student_btn.setEnabled(True)
            self.add_student_btn.setEnabled(True)
            self.delete_student_btn.setEnabled(True)

    # 5
    def delete_student(self):
        # Check if the CSV file exists
        if not os.path.exists(self.student_database):
            QMessageBox.warning(self, "Error", "No student has been added yet.")
            return
        
        # Check if there are data in the CSV file except the header
        with open(self.student_database, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            
            # Check if there are any rows excluding the header
            if len(list(reader)) <= 1:
                QMessageBox.warning(self, "Error", "No course has been added yet.")
                return
        
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
        # Check if the CSV file exists
        if not os.path.exists(self.student_database):
            QMessageBox.warning(self, "Error", "No student has been added yet.")
            return

        # Check if there are data in the CSV file except the header
        with open(self.student_database, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            
            # Check if there are any rows excluding the header
            if len(list(reader)) <= 1:
                QMessageBox.warning(self, "Error", "No course has been added yet.")
                return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("List of Students")
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.resize(400, 300)
        layout = QVBoxLayout(dialog)

        table = QTableWidget(dialog)
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
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Set cell as read-only
                table.setItem(i, j, item)

        table.resizeColumnsToContents()  # Adjust column widths
        table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)  # Adjust cell sizes to content

        layout.addWidget(table)
        dialog.exec()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())