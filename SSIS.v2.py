import sys
import mysql.connector

from PyQt6.QtWidgets import QApplication, QAbstractScrollArea, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog, QComboBox, QDialog, QTableWidget, QTableWidgetItem, QHeaderView, QFrame
from PyQt6.QtCore import Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSIS")
        self.setGeometry(100, 100, 1100, 500)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_frame = QVBoxLayout(self.central_widget)
               
        # Connect to MySQL database
        self.db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "root",
            database = "SSIS_database"
        )
        
        self.mycursor = self.db.cursor()
        
        self.create_course_table()  # Create the course table if it doesn't exist
        self.create_student_table() # Create the student table if it doesn't exist
        
        self.display_menu()
        
    # Course Table
    def create_course_table(self):
        self.mycursor.execute("""
             CREATE TABLE IF NOT EXISTS courses (
                course_code VARCHAR(20) NOT NULL PRIMARY KEY,
                course VARCHAR(100) NOT NULL
            )
        """)
        self.db.commit()
        
    # Student Table
    def create_student_table(self):
        self.mycursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id VARCHAR(50) NOT NULL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                gender VARCHAR(10) NOT NULL,
                year_level VARCHAR(10) NOT NULL,
                course_code VARCHAR(10),
                FOREIGN KEY (course_code) REFERENCES courses(course_code)
            )
        """)
        self.db.commit()            
        
    def display_menu(self):
        
        title_label = QLabel("Simple Student Information System")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "color: rgb(255, 255, 255);"  # Text color (white)
            "background-color: rgb(0, 0, 100);"  # Background color (indigo)
            "font-size: 30px;"  # Font size
            "font-weight: bold;"  # Font weight
            "font-family: 'Arial', sans-serif;"  # Font Style
        )
        
        

        # First column
        column1_layout = QVBoxLayout()
        
        self.add_course_btn = QPushButton("Add Course", self)
        self.add_course_btn.clicked.connect(self.add_course)
        column1_layout.addWidget(self.add_course_btn)
        
        self.list_course_btn = QPushButton("List of Course", self)
        self.list_course_btn.clicked.connect(self.list_course)
        column1_layout.addWidget(self.list_course_btn)
        
        self.update_course_btn = QPushButton("Update Course", self)
        self.update_course_btn.clicked.connect(self.update_course)
        column1_layout.addWidget(self.update_course_btn)
        
        self.delete_course_btn = QPushButton("Delete Course", self)
        self.delete_course_btn.clicked.connect(self.delete_course)
        column1_layout.addWidget(self.delete_course_btn)
        
        # Second column
        column2_layout = QVBoxLayout()
        
        self.add_student_btn = QPushButton("Add Student", self)
        self.add_student_btn.clicked.connect(self.add_student)
        column2_layout.addWidget(self.add_student_btn)
         
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
               
        # Creating New Layout with MainFrame (which is v_layout before)
        Inside_MainFrame = QHBoxLayout()
        self.main_frame.addLayout(Inside_MainFrame)  
        
        Left_IMF = QVBoxLayout()
        Inside_MainFrame.addLayout(Left_IMF)       
        Buttons_Left_IMF = QHBoxLayout()
        Buttons_Left_IMF.addLayout(column1_layout)
        Buttons_Left_IMF.addLayout(column2_layout)
        Left_IMF.addWidget(title_label)
        Left_IMF.addLayout(Buttons_Left_IMF)
        
        Right_IMF = QVBoxLayout()
        Inside_MainFrame.addLayout(Right_IMF)
  
        # Search bar widget
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search student...")
        Right_IMF.addWidget(search_bar)

        # Table widget
        table_widget = QTableWidget()
        table_widget.setColumnCount(5) 
        table_widget.setHorizontalHeaderLabels(["Student ID", "Name", "Gender", "Year Level", "Course Code"])
        Right_IMF.addWidget(table_widget)
        
        
        # Connect the search bar textChanged signal to search_students function
        search_bar.textChanged.connect(lambda text: self.search_students(text, table_widget))

    
    
    # Function to search students based on input text
    def search_students(self, search_text, table_widget):
        
        # 
        self.mycursor.execute("SELECT * FROM students WHERE student_id LIKE %s OR name LIKE %s OR gender LIKE %s OR year_level LIKE %s OR course_code LIKE %s",
                            (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))
        result = self.mycursor.fetchall()
        
        #Setup the table
        table_widget.clearContents()
        table_widget.setRowCount(len(result))
        for row, student in enumerate(result):
            for col, data in enumerate(student):
                item = QTableWidgetItem(str(data))
                table_widget.setItem(row, col, item)   
                     
    # A
    def add_course(self):
        
        # Getting input
        course_name, ok1 = QInputDialog.getText(self, 'Course Name', 'Enter course name:')
        if not ok1:
            return
        
        if course_name.strip() == "":
            QMessageBox.warning(self, 'Warning', 'Course name should not be blank.')
            return
        
        course_code, ok2 = QInputDialog.getText(self, 'Course Code', 'Enter course code:')
        if ok2:
            # Check if the course code already exists
            self.mycursor.execute("SELECT course_code FROM courses")
            course_codes = [row[0] for row in self.mycursor.fetchall()]
            
            if course_code in course_codes:
                QMessageBox.warning(self, "Error", "A course with the same code already exists!")
            elif not course_code:
                QMessageBox.warning(self, "Error", "Course code cannot be blank!")
            else:
                # Insert the course into the courses table
                insert_query = "INSERT INTO courses (course_code, course) VALUES (%s, %s)"
                values = (course_code, course_name)
                self.mycursor.execute(insert_query, values)
                self.db.commit()
                
                QMessageBox.information(self, 'Success', 'Course added successfully!')
        else:
            return
                
    # B
    def list_course(self):
    
        # Select all the courses from the courses table
        self.mycursor.execute("SELECT * FROM courses")
        courses = self.mycursor.fetchall()
        
        # Check if there are any courses
        if len(courses) == 0:
            QMessageBox.warning(self, "Error", "No course has been added yet.")
            return

        # Create a dialog window to display the list of courses
        dialog = QDialog(self)
        dialog.setWindowTitle("List of Courses")
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.resize(400, 300)
        layout = QVBoxLayout(dialog)

        table = QTableWidget(dialog)
        table.setColumnCount(2)  # Assuming there are 2 columns: course_code and course
        table.setHorizontalHeaderLabels(["Course Code", "Course"])
        table.verticalHeader().setVisible(False)
        
        table.setRowCount(len(courses))
        for i, course in enumerate(courses):
            for j in range(2):  # Assuming 2 columns
                item = QTableWidgetItem(str(course[j]))
                item.setFlags(item.flags() & Qt.ItemFlag.ItemIsEditable)  # Set cell as read-only
                table.setItem(i, j, item)

        table.resizeColumnsToContents()  # Adjust column widths
        table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)  # Adjust cell sizes to content
        layout.addWidget(table)
        dialog.adjustSize()  # Resize the dialog to fit the content
        
        dialog.exec()

    # C
    def update_course(self):
         # Check if any courses exist in the database
        self.mycursor.execute("SELECT course_code FROM courses")
        courses = self.mycursor.fetchall()
        if len(courses) == 0:
            QMessageBox.warning(self, "Error", "No course has been added yet.")
            return

        # Fetch the course codes from the database
        course_codes = [course[0] for course in courses]

        # Prompt the user to select the course code to update
        course_code, ok = QInputDialog.getItem(self, 'Update Course', 'Select course code:', course_codes, editable=False)
        if not ok:
            return

        # Prompt the user to select the update option
        options = ['Course Name', 'Course Code']
        choice, ok = QInputDialog.getItem(self, 'Update Course', 'Select option:', options, editable=False)
        if not ok:
            return

        if choice == 'Course Name':
            new_course_name, ok = QInputDialog.getText(self, 'Update Course', 'Enter new course name:')
            if not ok:
                return

            # Check for duplicates
            self.mycursor.execute("SELECT * FROM courses WHERE course = %s", (new_course_name,))
            duplicate_course = self.mycursor.fetchone()
            if duplicate_course:
                QMessageBox.warning(self, 'Error', 'The course name is already taken.')
                return

            # Check for blank input
            if not new_course_name:
                QMessageBox.warning(self, 'Error', 'Please enter a course name.')
                return
            
            # Update the course name in the database
            self.mycursor.execute("UPDATE courses SET course = %s WHERE course_code = %s", (new_course_name, course_code))
            self.db.commit()
            QMessageBox.information(self, 'Success', 'Course name updated successfully!')

        elif choice == 'Course Code':
            # Check if the course code is used in the students table
            self.mycursor.execute("SELECT * FROM students WHERE course_code = %s", (course_code,))
            students = self.mycursor.fetchall()
            if len(students) > 0:
                QMessageBox.warning(self, "Error", "The course is being used by one or more students. Cannot delete.")
                QMessageBox.warning(self, "Note", "If you want to proceed in updating the course, FIRST delete or update the students' course that use the course code.")
                return
            
            new_course_code, ok = QInputDialog.getText(self, 'Update Course', 'Enter new course code:')
            if not ok:
                return

            # Check for duplicates
            self.mycursor.execute("SELECT * FROM courses WHERE course_code = %s", (new_course_code,))
            duplicate_course = self.mycursor.fetchone()
            if duplicate_course:
                QMessageBox.warning(self, 'Error', 'The course code is already taken.')
                return

            # Check for blank input
            if not new_course_code:
                QMessageBox.warning(self, 'Error', 'Please enter a course code.')
                return
            
            # Update the course code in the database
            self.mycursor.execute("UPDATE courses SET course_code = %s WHERE course_code = %s", (new_course_code, course_code))
            self.db.commit()
            QMessageBox.information(self, 'Success', 'Course code updated successfully!')
                                           
    # D
    def delete_course(self):
        # Check if any courses exist in the database
        self.mycursor.execute("SELECT course_code FROM courses")
        courses = self.mycursor.fetchall()
        if len(courses) == 0:
            QMessageBox.warning(self, "Error", "No course has been added yet.")
            return

        # Fetch the course codes from the database
        course_codes = [course[0] for course in courses]

        # Prompt the user to select the course code to delete
        course_code, ok = QInputDialog.getItem(self, 'Delete Course', 'Select course code:', course_codes, editable=False)
        if not ok:
            return

        # Check if the course code is used in the students table
        self.mycursor.execute("SELECT * FROM students WHERE course_code = %s", (course_code,))
        students = self.mycursor.fetchall()
        if len(students) > 0:
            QMessageBox.warning(self, "Error", "The course is being used by one or more students. Cannot delete.")
            QMessageBox.warning(self, "Note", "If you want to proceed in deleting the course, FIRST delete or update the students' course that use the course code.")
            return
        
        # Delete the course from the database
        self.mycursor.execute("DELETE FROM courses WHERE course_code = %s", (course_code,))
        self.db.commit()
        QMessageBox.information(self, 'Success', 'Course deleted successfully!')
    
    
    
    
    # 1    
    def add_student(self):
        
        # Check if any courses exist in the database
        self.mycursor.execute("SELECT course_code FROM courses")
        courses = self.mycursor.fetchall()
        if len(courses) == 0:
            QMessageBox.warning(self, "Error", "No courses added yet!")
            return

        self.add_widget = QWidget()
        self.add_layout = QVBoxLayout(self.add_widget)

        self.add_label = QLabel("Add Student Information", self.add_widget)
        self.add_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.add_layout.addWidget(self.add_label)

        self.input_widgets = []
        
        # Create a QVBoxLayout to organize the fields vertically
        self.input_layout = QVBoxLayout()

        # Add Student ID field
        id_layout = QHBoxLayout()
        id_label = QLabel("Student ID:")
        id_line_edit = QLineEdit()
        id_line_edit.setPlaceholderText("xxxx-xxxx")
        id_layout.addWidget(id_label)
        id_layout.addWidget(id_line_edit)
        self.input_widgets.append(id_line_edit)
        self.input_layout.addLayout(id_layout)

        # Add Student Name field
        name_layout = QHBoxLayout()
        name_label = QLabel("Student Name:")
        name_line_edit = QLineEdit()
        name_line_edit.setPlaceholderText("First Name, Middle Initial, Last Name")  
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_line_edit)
        self.input_widgets.append(name_line_edit)
        self.input_layout.addLayout(name_layout)

        # Add Gender field
        gender_layout = QHBoxLayout()
        gender_label = QLabel("Gender:")
        gender_combo_box = QComboBox()
        gender_combo_box.addItems(["Male", "Female", "Other"])  
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(gender_combo_box)
        self.input_widgets.append(gender_combo_box)
        self.input_layout.addLayout(gender_layout)

        # Add Year Level field
        year_layout = QHBoxLayout()
        year_label = QLabel("Year Level:")
        year_combo_box = QComboBox()
        year_combo_box.addItems(["1st year", "2nd year", "3rd year", "4th year", "5th year", "6th year", "Other"])  
        year_layout.addWidget(year_label)
        year_layout.addWidget(year_combo_box)
        self.input_widgets.append(year_combo_box)
        self.input_layout.addLayout(year_layout)

        # Add Course Code field
        course_layout = QHBoxLayout()
        course_label = QLabel("Course Code:")
        combo_box = QComboBox()
        combo_box.addItems([course[0] for course in courses])
        course_layout.addWidget(course_label)
        course_layout.addWidget(combo_box)
        self.input_widgets.append(combo_box)
        self.input_layout.addLayout(course_layout)

       # Add Submit button
        button_layout = QHBoxLayout()
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.save_student)
        button_layout.addWidget(self.submit_btn)
        
       # Add Back button
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.delete_form)
        button_layout.addWidget(self.back_btn)

        self.input_layout.addLayout(button_layout)
        self.add_layout.addLayout(self.input_layout)
        
        # Disable all the other buttons
           # Courses button
        self.add_course_btn.setDisabled(True)
        self.list_course_btn.setDisabled(True)
        self.update_course_btn.setDisabled(True)
        self.delete_course_btn.setDisabled(True)
        
           # Student buttons
        self.add_student_btn.setDisabled(True)
        self.search_id_btn.setDisabled(True)
        self.search_name_btn.setDisabled(True)
        self.update_student_btn.setDisabled(True)
        self.delete_student_btn.setDisabled(True)
        self.list_student_btn.setDisabled(True)

        self.main_frame.addWidget(self.add_widget)
        
    # 1.A    
    def delete_form(self):
        self.main_frame.removeWidget(self.add_widget)
        self.add_widget.deleteLater()
        
        # Enable all the other buttons back
           # Courses button
        self.add_course_btn.setEnabled(True)
        self.list_course_btn.setEnabled(True)
        self.update_course_btn.setEnabled(True)
        self.delete_course_btn.setEnabled(True)
        
           # Student buttons
        self.add_student_btn.setEnabled(True)
        self.search_id_btn.setEnabled(True)
        self.search_name_btn.setEnabled(True)
        self.update_student_btn.setEnabled(True)
        self.delete_student_btn.setEnabled(True)
        self.list_student_btn.setEnabled(True)

        # Clear the input fields
        for widget in self.input_widgets:
            widget.clear()


        
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

        # Validate student ID length
        max_id_length = 50
        student_id = str(student_data[0]).strip()
        if len(student_id) > max_id_length:
            QMessageBox.warning(self, "Error", f"Student ID should not exceed {max_id_length} characters!")
            return

        # Check if student with the same student_id already exists
        query = "SELECT * FROM students WHERE student_id = %s"
        self.mycursor.execute(query, (student_id,))
        existing_students = self.mycursor.fetchall()
        if existing_students:
            QMessageBox.warning(self, "Error", "A student with the same ID already exists!")
            return

        # Insert new student into the database
        insert_query = "INSERT INTO students (student_id, name, gender, year_level, course_code) VALUES (%s, %s, %s, %s, %s)"
        values = (student_id, student_data[1], student_data[2], student_data[3], student_data[4])
        self.mycursor.execute(insert_query, values)
        self.db.commit()
        
        QMessageBox.information(self, "Success!", "Student information saved successfully")
        
        self.main_frame.removeWidget(self.add_widget)
        self.add_widget.deleteLater()
        
        # Enable all the other buttons back
           # Courses button
        self.add_course_btn.setEnabled(True)
        self.list_course_btn.setEnabled(True)
        self.update_course_btn.setEnabled(True)
        self.delete_course_btn.setEnabled(True)
        
           # Student buttons
        self.add_student_btn.setEnabled(True)
        self.search_id_btn.setEnabled(True)
        self.search_name_btn.setEnabled(True)
        self.update_student_btn.setEnabled(True)
        self.delete_student_btn.setEnabled(True)
        self.list_student_btn.setEnabled(True)
    
        self.main_frame.removeWidget(self.add_widget)
        self.add_widget.deleteLater()
     
       
    # 2
    def search_ID_student(self):  
        # Check if the students table exists
        self.mycursor.execute("SHOW TABLES LIKE 'students'")
        table_exists = self.mycursor.fetchone()
        if not table_exists:
            QMessageBox.warning(self, "Error", "No student has been added yet.")
            return
        
        # Get the ID to search from user input
        student_id, ok = QInputDialog.getText(self, "Search Student", "Enter the ID to search:")
        if ok:
            # Query the database for the student with the given ID
            query = "SELECT * FROM students WHERE student_id = %s"
            self.mycursor.execute(query, (student_id,))
            student_data = self.mycursor.fetchone()

            if student_data:
                self.show_student_info(student_data)
            else:
                QMessageBox.information(self, "Not Found", "ID not found in our database.")

    # 3
    def search_name_student(self):
        # Check if the students table exists
        self.mycursor.execute("SHOW TABLES LIKE 'students'")
        table_exists = self.mycursor.fetchone()
        if not table_exists:
            QMessageBox.warning(self, "Error", "No student has been added yet.")
            return
        
        # Get the name to search from user input
        name, ok = QInputDialog.getText(self, "Search Student", "Enter the name to search:")
        if ok:
            
            # Query the database for the student with the given name
            query = "SELECT * FROM students WHERE name = %s"
            self.mycursor.execute(query, (name,))
            student_data = self.mycursor.fetchone()

            if student_data:
                self.show_student_info(student_data)
            else:
                QMessageBox.information(self, "Not Found", "Name not found in our database.")
        
    # 3&4.A    
    def get_input(self, message):
        text, ok = QInputDialog.getText(self, 'Input Dialog', message)
        if ok:
            return text
    
    # 3&4.B 
    def show_student_info(self, student):
        info = f"Name: {student[1]}\nID: {student[0]}\nGender: {student[2]}\nYear Level: {student[3]}\nCourse Code: {student[4]}"
        self.show_message_box(info)

    # 3&4.C
    def show_message_box(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Message")
        msg_box.setText(message)
        msg_box.exec()            

    # 4
    def update_student(self):
        # Select all the students from the students table
        self.mycursor.execute("SELECT * FROM students")
        students = self.mycursor.fetchall()
        
        # Check if there are any students 
        if len(students) == 0:
            QMessageBox.warning(self, "Error", "No student has been added yet.")
            return

        self.id, ok = QInputDialog.getText(self, "Update Student", "Enter ID to update")
        if ok:
            # Check if the student with the given ID exists
            query = "SELECT * FROM students WHERE student_id = %s"
            self.mycursor.execute(query, (self.id,))
            existing_student = self.mycursor.fetchone()
            if not existing_student:
                QMessageBox.warning(self, "Error", "ID not found in our database")
                return
            
            # Disable all the other buttons
                # Courses button
            self.add_course_btn.setDisabled(True)
            self.list_course_btn.setDisabled(True)
            self.update_course_btn.setDisabled(True)
            self.delete_course_btn.setDisabled(True)
            
                # Student buttons
            self.add_student_btn.setDisabled(True)
            self.search_id_btn.setDisabled(True)
            self.search_name_btn.setDisabled(True)
            self.update_student_btn.setDisabled(True)
            self.delete_student_btn.setDisabled(True)
            self.list_student_btn.setDisabled(True)

            self.display_update_form(existing_student)

    # 4.A
    def display_update_form(self, student):
        self.update_widget = QWidget()
        self.update_layout = QVBoxLayout(self.update_widget)

        self.mycursor.execute("SELECT course_code FROM courses")
        courses = self.mycursor.fetchall()

        self.input_widgets = []
        self.student_fields = ['Student ID', 'Student Name', 'Gender', 'Year Level', 'Course Code']
        db_field_names = ['student_id', 'name', 'gender', 'year_level', 'course_code']

        for field, db_field, value in zip(self.student_fields, db_field_names, student):
            h_layout = QHBoxLayout()
            label = QLabel(field, self.update_widget)

            if field == 'Course Code':
                combo_box = QComboBox(self.update_widget)
                combo_box.addItems([course[0] for course in courses])
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

            self.update_layout.addLayout(h_layout)

        update_button = QPushButton("Update", self.update_widget)
        update_button.clicked.connect(self.update_student_data)
        self.update_layout.addWidget(update_button)

        back_button = QPushButton("Back", self.update_widget)
        back_button.clicked.connect(self.erase_update_form)
        self.update_layout.addWidget(back_button)

        self.main_frame.addWidget(self.update_widget)

    # 4.B
    def update_student_data(self):
        student_data = []
        for widget in self.input_widgets:
            data = widget.currentText() if isinstance(widget, QComboBox) else widget.text()
            if not data:
                QMessageBox.warning(self, "Error", "Please fill in all fields!")
                return
            student_data.append(data)
        
        # Validate student ID length
        max_id_length = 50
        student_id = str(student_data[0]).strip()
        if len(student_id) > max_id_length:
            QMessageBox.warning(self, "Error", f"Student ID should not exceed {max_id_length} characters!")
            return

        # Check if a student with the same student_id already exists
        query = "SELECT * FROM students WHERE student_id = %s"
        self.mycursor.execute(query, (student_id,))
        existing_students = self.mycursor.fetchall()
        if existing_students and student_id != existing_students[0][0]:
            QMessageBox.warning(self, "Error", "A student with the same ID already exists!")
            return
        
        # Update the students from the database
        update_query = "UPDATE students SET student_id = %s, name = %s , gender = %s, year_level = %s, course_code = %s WHERE student_id = %s"
        values = (student_data[0], student_data[1], student_data[2], student_data[3], student_data[4], self.id )
        self.mycursor.execute(update_query, values)
        self.db.commit()
        
        self.show_message_box(f'Student with ID {self.id} has been updated successfully')
        self.erase_update_form()
        
    # 4.C
    def erase_update_form(self):
        if self.update_widget:
            self.main_frame.removeWidget(self.update_widget)
            self.update_widget.deleteLater()
            self.update_widget = None
            
        # Enable all the other buttons back
           # Courses button
        self.add_course_btn.setEnabled(True)
        self.list_course_btn.setEnabled(True)
        self.update_course_btn.setEnabled(True)
        self.delete_course_btn.setEnabled(True)
        
           # Student buttons
        self.add_student_btn.setEnabled(True)
        self.search_id_btn.setEnabled(True)
        self.search_name_btn.setEnabled(True)
        self.update_student_btn.setEnabled(True)
        self.delete_student_btn.setEnabled(True)
        self.list_student_btn.setEnabled(True)

    # 5
    def delete_student(self):
        # Select all the students from the students table
        self.mycursor.execute("SELECT * FROM students")
        students = self.mycursor.fetchall()
        
        # Check if there are any students 
        if len(students) == 0:
            QMessageBox.warning(self, "Error", "No student has been added yet.")
            return
        
        id, ok = QInputDialog.getText(self, "Enter ID", "Enter the ID of the student to delete:")
    
        if ok:
            # Check if the student with the given ID exists
            query = "SELECT * FROM students WHERE student_id = %s"
            self.mycursor.execute(query, (id,))
            existing_student = self.mycursor.fetchone()
            if not existing_student:
                self.show_message_box(f'Student with ID {id} not found in the database')
                return

            # Delete the student from the database
            delete_query = "DELETE FROM students WHERE student_id = %s"
            self.mycursor.execute(delete_query, (id,))
            self.db.commit()
            self.show_message_box(f'Student with ID {id} has been deleted successfully')
            
        else:
            return
    # 6        
    def list_students(self):
        # Select all the students from the students table
        self.mycursor.execute("SELECT * FROM students")
        students = self.mycursor.fetchall()

        # Check if there are any students 
        if len(students) == 0:
            QMessageBox.warning(self, "Error", "No student has been added yet.")
            return

        # Create a dialog window to display the list of students
        dialog = QDialog(self)
        dialog.setWindowTitle("List of Students")
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.resize(400, 300)
        layout = QVBoxLayout(dialog)

        table = QTableWidget(dialog)
        table.setColumnCount(5)  # Number of fields
        table.setHorizontalHeaderLabels(["Student ID", "Name", "Gender", "Year Level", "Course Code"])
        table.verticalHeader().setVisible(True)

        table.setRowCount(len(students))
        for i, row_data in enumerate(students):
            for j, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Set cell as read-only
                table.setItem(i, j, item)


        table.resizeColumnsToContents()  # Adjust column widths
        table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)  # Adjust cell sizes to content
        layout.addWidget(table)
        dialog.adjustSize()  # Resize the dialog to fit the content
        
        dialog.exec()
        
if __name__ == '__main__':
    import sys
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())