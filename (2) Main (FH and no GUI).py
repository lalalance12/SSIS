# Simple Student Information System with file Handling
 
import csv
# Define global variables
student_fields = ['Name', 'ID', 'Course']
student_database = 'Students Information.csv'
 
 
def display_menu():
    print("--------------------------------------")
    print(" Welcome to Student Information System")
    print("--------------------------------------")
    print("     ")
    print("1. Add Student")
    print("2. Search Student by ID")
    print("3. Search Student by name")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. List Student")
    print("7. Quit")
 
def add_student():
    print("         ")
    print("-------------------------")
    print("Add Student Information")
    print("-------------------------")
    print("         ")
    global student_fields
    global student_database
 
    student_data = []
    for field in student_fields:
        value = input("Enter " + field + ": ")
        student_data.append(value)
 
    with open(student_database, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows([student_data])
    
    print("     ")
    print("Data saved successfully")
    print("     ")        
    print("-----------------------")
    input("Press enter to continue")
    print("-----------------------")
    print("     ")
    return
    
 
 
def search_ID_student():
    global student_fields
    global student_database
 
    print("--- Search Student ---")
    id = input("Enter ID number to search: ")
    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0:
                if id == row[1]:
                    print("         ")
                    print("         ")
                    print("----- Student Found -----")
                    print("----- Student Found -----")
                    print("Name: ", row[0])
                    print("Id: ", row[1])
                    print("Course: ", row[2])
                    break
        else:
            print("         ")
            print("ID number not found in our database")
            
            
    print("     ")        
    print("-----------------------")
    input("Press enter to continue")
    print("-----------------------")
    print("     ")

def search_name_student():
    global student_fields
    global student_database
 
    print("--- Search Student ---")
    id = input("Enter name number to search: ")
    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0:
                if id == row[0]:
                    print("         ")
                    print("         ")
                    print("----- Student Found -----")
                    print("Name: ", row[0])
                    print("Id: ", row[1])
                    print("Course: ", row[2])
                    break
        else:
            print("         ")
            print("Name not found in our database")
            
    print("     ")        
    print("-----------------------")
    input("Press enter to continue")
    print("-----------------------")
    print("     ")
 
def update_student():
    global student_fields
    global student_database
 
    print("--- Update Student ---")
    id = input("Enter ID number to update: ")
    index_student = None
    updated_data = []
    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        counter = 0
        for row in reader:
            if len(row) > 0:
                if id == row[1]:
                    index_student = counter
                    print("Student Found: at index ",index_student)
                    student_data = []
                    for field in student_fields:
                        value = input("Enter " + field + ": ")
                        student_data.append(value)
                    updated_data.append(student_data)
                else:
                    updated_data.append(row)
                counter += 1
 
 
    # Check if the record is found or not
    if index_student is not None:
        with open(student_database, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(updated_data)
    else:
        print("         ")
        print("ID number not found in our database")
    
    print("     ")        
    print("-----------------------")
    input("Press enter to continue")
    print("-----------------------")
    print("     ")
 
 
def delete_student():
    global student_fields
    global student_database
 
    print("--- Delete Student ---")
    id = input("Enter ID number to delete: ")
    student_found = False
    updated_data = []
    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        counter = 0
        for row in reader:
            if len(row) > 0:
                if id != row[1]:
                    updated_data.append(row)
                    counter += 1
                else:
                    student_found = True
 
    if student_found is True:
        with open(student_database, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(updated_data)
        print("ID number", id, "deleted successfully")
    else:
        print("         ")
        print("ID number not found in our database")
    
    print("     ")        
    print("-----------------------")
    input("Press enter to continue")
    print("-----------------------")
    print("     ")
    
def view_students():
    global student_fields
    global student_database
 
    print("--- Student Records ---")
 
    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for x in student_fields:
            print(x, end='\t |')
        print("\n-----------------------------------------------------------------")
 
        for row in reader:
            for item in row:
                print(item, end="\t|")
            print("\n")
    
    print("     ")        
    print("-----------------------")
    input("Press enter to continue")
    print("-----------------------")
    print("     ")
 
 
while True:
    display_menu()
 
    choice = input("Enter your choice: ")
    if choice == '1':
        add_student()
    elif choice == '2':
        search_ID_student()
    elif choice == '3':
        search_name_student()
    elif choice == '4':
        update_student()
    elif choice == '5':
        delete_student()
    elif choice == '6':
        view_students()
    elif choice == "7":
        print("   ")
        print("-----------------")
        print("  Exited SIS :(  ")
        print("-----------------")
        print("   ")
        break
    else:
        print("   ")
        print("-----------------------")
        print("Invalid input try again")
        print("-----------------------")
        print("   ")
        
        print("     ")        
        print("-----------------------")
        input("Press enter to continue")
        print("-----------------------")
        print("     ")
 
