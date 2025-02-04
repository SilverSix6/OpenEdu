from src.Database.Query.DatabaseQueryAll import DatabaseQueryAll;
from src.Database.DatabaseManager import DatabaseManager;
import mysql

class SelectAllInstructors(DatabaseQueryAll):
    @classmethod
    def queryAll(cls) -> list:
        #This method gets all instructors in database and returns their id
        #and their firstName + lastName. Used to show all professors
        #in drop down menu when creating courses
        cursor = DatabaseManager.getDatabaseCursor()

        statement = "SELECT Instructor.userId, User.firstName, User.lastName FROM Instructor LEFT JOIN User ON Instructor.userId = User.userId" 
        cursor.execute(statement)
        instructorData = cursor.fetchall()

        #Extracting ids,names from their respective columns
        instructorId = [row[0] for row in instructorData]
        instructorName = [row[1] +" "+ row[2] for row in instructorData]
        return instructorId, instructorName


