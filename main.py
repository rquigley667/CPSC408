import sqlite3
import csv
import sys


conn = sqlite3.connect('/Users/reesequigley/CPSC408/Assignment1_CPSC408/StudentDB.db')
mycursor = conn.cursor()


studentData = "students.csv"
StudentId = 0

mycursor.execute("CREATE TABLE IF NOT EXISTS student( StudentId INTEGER PRIMARY KEY ,FirstName TEXT, LastName TEXT , GPA REAL , Major TEXT , FacultyAdvisor TEXT , Address TEXT , City TEXT , State TEXT , ZipCode TEXT , MobilePhoneNumber TEXT, isDeleted TEXT )")
conn.commit()


with open(studentData, 'r+') as csvfile:
 studentDataCSV = csv.reader(csvfile)
 header = next(studentDataCSV)
 for row in studentDataCSV:
     if len(row) >= 12:
         StudentId = row[0] if len(row) > 0 else ''
     FirstName = (row[1])
     LastName = (row[2])
     GPA = (row[3])
     Major = (row[4])
     FacultyAdvisor = (row[5])
     Address = (row[6])
     City = (row[7])
     State = (row[8])
     ZipCode = row[9] if len(row) > 9 else ''
     MobilePhoneNumber = (row[10]) if len(row) > 10 else ''
     isDeleted = row[11] if len(row) > 11 else ''


     mycursor.execute("SELECT StudentId FROM student WHERE StudentId = ?", (StudentId,))
     existing_student = mycursor.fetchone()


     mycursor.execute(
         "UPDATE student SET FirstName = ?, LastName = ?, GPA = ?, Major = ?, FacultyAdvisor = ?, Address = ?, City = ?, State = ?, ZipCode = ?, MobilePhoneNumber = ?, isDeleted = ? WHERE StudentId = ?",
         (StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber,
          isDeleted))




def selectStudents():
    mycursor.execute("SELECT * FROM Student;")
    rows = mycursor.fetchall()
    for row in rows:
        print(row)
#selectStudents()
#mycursor.close()


def addStudent():
    if sys.version_info.major == 2:

        studentID = raw_input("Enter StudentId: ")
        firstName = raw_input("Enter FirstName: ")
        lastName = raw_input("Enter LastName: ")
        GPA = float(raw_input("Enter GPA: "))  # Convert input to float
        major = raw_input("Enter Major: ")
        FacultyAdvisor = raw_input("Enter Faculty Advisor: ")
        Address = raw_input("Enter Address: ")
        City = raw_input("Enter City: ")
        State = raw_input("Enter State: ")
        ZipCode = raw_input("Enter Zipcode: ")
        MobilePhoneNumber = raw_input("Enter Phone Number: ")
        isDeleted = input("Do you want to delete this student? ")

    else:
        studentID = input("Enter StudentId: ")
        firstName = input("Enter FirstName: ")
        lastName = input("Enter LastName: ")
        while True:
            try:
                GPA = float(input("Enter GPA: "))
                if 0.0 <= GPA <= 4.0:
                    break
                else:
                    print("GPA must be between 0.0 and 4.0.")
            except ValueError:
                print("Invalid GPA input. Please enter a valid number.")
        major = input("Enter Major: ")
        FacultyAdvisor = input("Enter Faculty Advisor: ")
        Address = input("Enter Address: ")
        City = input("Enter City: ")
        #State = input("Enter State: ")
        ZipCode = input("Enter Zipcode: ")
        MobilePhoneNumber = input("Enter Phone Number: ")
        isDeleted = input("Do you want to delete this student? ")


    insert_query = "INSERT INTO Student (studentId, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber,isDeleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)"
    values = (
        studentID, firstName, lastName, GPA, major, FacultyAdvisor, Address, City, State, ZipCode,
        MobilePhoneNumber,isDeleted)

    mycursor.execute(insert_query, values)
    conn.commit()
#addStudent()
#mycursor.close()


def updateStudent():
    studentID = input("Enter StudentId to update: ")

    field_to_update = input("Enter the field to update('Major','FacultyAdvisor','MobilePhoneNumber')(put the '' in your answer): ").strip()

    allowed_fields = ['Major', 'FacultyAdvisor', 'MobilePhoneNumber']
    if field_to_update not in allowed_fields:
        print("Invalid field. Please enter Major, FacultyAdvisor, or MobilePhoneNumber.")
        return

    new_value = input("Enter the new " + field_to_update + ":(Put it in '') ")

    update_query = "UPDATE Student SET " + field_to_update + " = ? WHERE studentId = ?"
    values = (new_value, studentID)

    mycursor.execute(update_query, values)
    conn.commit()

    if mycursor.rowcount == 0:
        print("No matching student found for the provided StudentId: .")
    else:
        print("Student with StudentId has been updated.")





def DeleteStudent(StudentId):
    StudentId = int(input("Enter the student ID you want to delete: "))

    mycursor.execute("DELETE FROM student WHERE StudentId = ?", (StudentId,))
    conn.commit()

    if mycursor.rowcount == 1:
        print("Student  has been deleted.")
    else:
        print("Student with ID {StudentId} not found.")







def searchStudentsByCriteria(student_list):
    print("Search/Display Students by Major, GPA, City, State, or Advisor")

    major = input("Enter Major(Put in quotation marks and lower case): ").strip().lower()
    gpa = input("Enter GPA: ")
    city = input("Enter City(Put in quotation marks and lower case): ").strip().lower()
    state = input("Enter State(Put in quotation marks and lower case): ").strip().lower()
    advisor = input("Enter Advisor(Put in quotation marks and lower case): ").strip().lower()

    matching_students = []

    for student in student_list:
        student_major = student['Major'].lower()
        student_city = student['City'].lower()
        student_state = student['State'].lower()
        student_advisor = student['Advisor'].lower()

        if (not major or major in student_major) and \
           (not gpa or str(gpa) == str(student['GPA'])) and \
           (not city or city in student_city) and \
           (not state or state in student_state) and \
           (not advisor or advisor in student_advisor) and \
           not student.get('isDeleted', False):
            matching_students.append(student)

    if not matching_students:
        print("No matching students found.")
    else:
        print("Matching students:")
        for student in matching_students:  # Iterate through matching_students list
            print("ID: {}, Major: {}, GPA: {}, City: {}, State: {}, Advisor: {}".format(
                student['ID'], student['Major'], student['GPA'], student['City'], student['State'], student['Advisor']
            ))

# Example usage:
students = [
    {"ID": 1, "Major": "Computer Science", "GPA": 3.5, "City": "New York", "State": "NY", "Advisor": "Dr. Smith"},
    {"ID": 2, "Major": "Biology", "GPA": 3.2, "City": "Los Angeles", "State": "CA", "Advisor": "Dr. Johnson"},
    {"ID": 3, "Major": "computer scince", "GPA": 4.0, "City": "Ornge", "State": "CA", "Advisor": "Jonh"},
    {"ID": 4, "Major": "StephenMouth", "GPA": 2.7, "City": "Los Angeles", "State": "CA", "Advisor": "Null"},
]
#searchStudentsByCriteria(students)

def exitProgram():
    print("Exiting out of the application")
    sys.exit(0)
#exitProgram()




def main():
    while True:
        print("Press 1 to see all the students and their attributes.\n"
                       "Press 2 to add a student.\n"
                       "Press 3 to update a student record.\n"
                       "Press 4 to delete a student from the record.\n"
                       "Press 5 to Exit out of application.\n")
        UserOptionSelected = input("You want: ")

        if UserOptionSelected == 1:
            selectStudents()
        elif UserOptionSelected == 2:
            addStudent()
        elif UserOptionSelected == 3:
            updateStudent()
        elif UserOptionSelected == 4:
            DeleteStudent(StudentId)
        elif UserOptionSelected == 5:
            exitProgram()
        else:
            print("Has to be one of these options!!")

if __name__ == "__main__":
    main()
