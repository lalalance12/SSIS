students = {}  # initialize an empty dictionary to store student information

# function to add a new student to the system
def add_student():
    print("Enter the details of the student:")
    name = input("Name: ")
    id = input("ID: ")
    course = input("Course: ")
    students[id] = {"name": name, "course": course}
    print("Student added successfully!")
    
# function to edit an existing student's information
def edit_student():
    id = input("Enter the ID of the student you want to edit: ")
    if id in students:
        print("Enter the new details of the student:")
        name = input("Name: ")
        course = input("Course: ")
        students[id]["name"] = name
        students[id]["course"] = course
        print("Student information updated successfully!")
    else:
        print("Student with ID", id, "not found.")
        
# function to delete an existing student from the system
def delete_student():
    id = input("Enter the ID of the student you want to delete: ")
    if id in students:
        del students[id]
        print("Student deleted successfully!")
    else:
        print("Student with ID", id, "not found.")
        
# function to list all the students in the system
def list_students():
    print("List of students:")
    for id, info in students.items():
        print(id, "-", info["name"], "-", info["course"])
        
# function to search for a student by name
def search_by_name():
    name = input("Enter the name of the student you want to search for: ")
    found = False
    for id, info in students.items():
        if info["name"].lower() == name.lower():
            print("Student found:")
            print(id, "-", info["name"], "-", info["course"])
            found = True
    if not found:
        print("Student with name", name, "not found.")
        
# function to search for a student by ID
def search_by_id():
    id = input("Enter the ID of the student you want to search for: ")
    if id in students:
        info = students[id]
        print("Student found:")
        print(id, "-", info["name"], "-", info["course"])
    else:
        print("Student with ID", id, "not found.")

# function to search for students by course
def search_by_course():
    course = input("Enter the course name to search for: ")
    found = False
    for id, info in students.items():
        if info["course"].lower() == course.lower():
            print("Student found:")
            print(id, "-", info["name"], "-", info["course"])
            found = True
    if not found:
        print("No students found for course", course)
        
# main program loop
while True:
    print("\nStudent Information System")
    print("1. Add Student")
    print("2. Edit Student")
    print("3. Delete Student")
    print("4. List Students")
    print("5. Search by Name")
    print("6. Search by ID")
    print("7. Search by Course")
    print("8. Exit")
    
    choice = input("Enter your choice (1-8)") 
    
    if choice == "1":
        add_student()
    elif choice == "2":
        edit_student()
    elif choice == "3":
        delete_student()
    elif choice == "4":
        list_students()
    elif choice == "5":
        search_by_name()
    elif choice == "6":
        search_by_id()
    elif choice == "7":
        search_by_course()
    elif choice == "8":
        print("Exited SIS")
        break
        
        