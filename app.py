
from flask import Flask, render_template, redirect, url_for, request

import mysql.connector
from pythonFiles.DatabaseManager import DatabaseManager
from pythonFiles.User import User

currentUser = None #Start with no user logged in
app = Flask(__name__)

# Database configuration
# Should put this in a config file but eh
db_config = {
    'user': 'team',
    'password': 'COSC310Team',
    'host': '50.98.157.215',
    'port': '3306',
    'database': 'openEDU'
}

# Establish a database connection
db = mysql.connector.connect(**db_config)


@app.route("/")
def home():
    # Test the database connection
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")  # Simple query to test
    db_version = cursor.fetchone()
    cursor.close()
    return render_template("template.html", db_version=db_version)
    
@app.route("/login")
def login():
    return render_template("login.html");

@app.route("/login/createaccount", methods=['GET', 'POST'])
def createAccount():
    # Default handeling of page
    if (request.method == 'GET'):
        return render_template("accountCreation.html");
    # Post request occures when form is submitted
    else: # Post Request
        createUser = ("INSERT INTO User (firstName, lastName, email, password, username) VALUES (%s, %s, %s, %s, %s);");
        createTeacher = ("INSERT INTO Instructor (userId) VALUES (LAST_INSERT_ID());");
        createStudent = ("INSERT INTO Student (userId) VALUES (LAST_INSERT_ID());");
        
        # Retrieve form data
        form = request.form;
        userData = (form['fname'],form['lname'],form['email'],form['password'], form['uname']);
        
        cursor = db.cursor();
        
        cursor.execute(createUser, userData);
        
        # Create a student or instructor account depending on user's choice 
        if (form['accountType'] == 'student'):
            cursor.execute(createStudent);
        else:
            cursor.execute(createTeacher);
        
        db.commit();
        
        # Forward to the login page
        return login();
        

@app.route("/authenticate", methods=['POST'])
def authenticate():
    #Get inputted username and password from user
    username = request.form.get('uname')
    password = request.form.get('password')

    #Check if user exists in database
    database = DatabaseManager()
    validLogin = database.checkLogin(username, password)

    #If exists, bring back to home page, ow stay on login page
    if validLogin:
        #Create User class that stores data for current logged-in user
        SData = database.selectStudentUserPass(username, password)
        currentUser = User(SData[0], SData[1], SData[2], SData[3], SData[4], SData[5]) 
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
    
@app.route("/seeGrades", methods=['GET'])
def seeGrades(): 
    # Query for getting grades for every assignment in a class for a given student
    getGrades = "SELECT Assignment.assignmentId, name, grade, comment FROM Assignment JOIN Grades ON Assignment.assignmentId = Grades.assignmentId WHERE studentId = %s AND courseId = %s"
    # Query for getting the course name
    getCourseName = "SELECT name FROM Course WHERE courseId  = %s"
    
    cursor = db.cursor()
    cursor.execute(getGrades, ("1","1",)) # Test, change later
    grades = cursor.fetchall()
    cursor.close()
    cursor = db.cursor()
    cursor.execute(getCourseName, ("1",)) # Test, change later
    courseName = cursor.fetchone()
    cursor.close()
    
    # Go to See Grades page
    return render_template("seeGrades.html", grades=grades, courseName=courseName)

@app.route("/courseRegistration")
def courseRegistration():
    return render_template("courseRegistration.html")
if __name__ == "__main__":
    app.run()
