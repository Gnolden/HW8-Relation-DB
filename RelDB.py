import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('sqlite3.db')
cursor = conn.cursor()

# Drop existing tables if they exist (for testing purposes)
cursor.executescript('''
DROP TABLE IF EXISTS Advisor;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Student_Advisor;
''')

# Create tables
cursor.executescript('''
CREATE TABLE Advisor( 
    AdvisorID INTEGER NOT NULL PRIMARY KEY, 
    AdvisorName TEXT NOT NULL
);

CREATE TABLE Student( 
    StudentID INTEGER NOT NULL PRIMARY KEY, 
    StudentName TEXT NOT NULL
);

CREATE TABLE Student_Advisor(
    StudentID INTEGER,
    AdvisorID INTEGER,
    FOREIGN KEY(StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY(AdvisorID) REFERENCES Advisor(AdvisorID),
    PRIMARY KEY(StudentID, AdvisorID)
);
''')

# Populate tables with sample data
cursor.executescript('''
INSERT INTO Advisor(AdvisorID, AdvisorName) VALUES 
(1,"John Paul"), 
(2,"Anthony Roy"), 
(3,"Raj Shetty"), 
(4,"Sam Reeds"), 
(5,"Arthur Clintwood");

INSERT INTO Student(StudentID, StudentName) VALUES 
(501,"Geek1"), 
(502,"Geek2"), 
(503,"Geek3"), 
(504,"Geek4"), 
(505,"Geek5"), 
(506,"Geek6"), 
(507,"Geek7"), 
(508,"Geek8"), 
(509,"Geek9"), 
(510,"Geek10");

INSERT INTO Student_Advisor(StudentID, AdvisorID) VALUES 
(501, 1), 
(502, 1), 
(503, 3), 
(504, 2), 
(505, 4), 
(506, 2), 
(507, 2), 
(508, 3), 
(509, NULL), 
(510, 1);
''')

# Retrieve list of advisors with the number of their students
cursor.execute('''
SELECT Advisor.AdvisorID, Advisor.AdvisorName, COUNT(Student_Advisor.StudentID) AS NumStudents
FROM Advisor
LEFT JOIN Student_Advisor ON Advisor.AdvisorID = Student_Advisor.AdvisorID
GROUP BY Advisor.AdvisorID
ORDER BY Advisor.AdvisorID
''')

# Print the result
print("List of Advisors with Number of Students:")
for row in cursor.fetchall():
    advisor_id, advisor_name, num_students = row
    print(f"Advisor ID: {advisor_id}, Name: {advisor_name}, Number of Students: {num_students}")

# Commit changes to database
conn.commit()

# Closing the connection
conn.close()
