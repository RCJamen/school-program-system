DROP DATABASE IF EXISTS `progsys_db`;
CREATE DATABASE IF NOT EXISTS `progsys_db`;
use `progsys_db`;

-- NOT USED
-- DROP TABLE IF EXISTS `colleges`;
-- CREATE TABLE IF NOT EXISTS `colleges`(
-- collegeID INT AUTO_INCREMENT NOT NULL,
-- name VARCHAR(255) NOT NULL,
-- PRIMARY KEY(collegeID)
-- );

-- NOT USED
-- DROP TABLE IF EXISTS `curriculum`;
-- CREATE TABLE IF NOT EXISTS `curriculum`(
-- currID INT AUTO_INCREMENT NOT NULL,
-- name VARCHAR(255) NOT NULL,
-- description CHAR NOT NULL,
-- PRIMARY KEY(currID)
-- );

-- NOT USED
-- DROP TABLE IF EXISTS `departments`;
-- CREATE TABLE IF NOT EXISTS `departments`(
-- departmentID INT AUTO_INCREMENT NOT NULL,
-- name VARCHAR(255) NOT NULL,
-- collegeID INT NOT NULL,
-- currID INT NOT NULL,
-- PRIMARY KEY(departmentID),
-- FOREIGN KEY(collegeID) REFERENCES colleges(collegeID),
-- FOREIGN KEY(currID) REFERENCES curriculum(currID)
-- );

-- NOT USED
-- DROP TABLE IF EXISTS `learning_outcomes`;
-- CREATE TABLE IF NOT EXISTS `learning_outcomes`(
-- learnOutID INT AUTO_INCREMENT NOT NULL,
-- title VARCHAR(255) NOT NULL,
-- description CHAR NOT NULL,
-- currID INT NOT NULL,
-- PRIMARY KEY(learnOutID),
-- FOREIGN KEY(currID) REFERENCES curriculum(currID)
-- );


-- NOT USED
-- DROP TABLE IF EXISTS `student_outcomes`;
-- CREATE TABLE IF NOT EXISTS `student_outcomes`(
-- stuOutID INT AUTO_INCREMENT NOT NULL,
-- name VARCHAR(255) NOT NULL,
-- description CHAR NOT NULL,
-- assessID INT NOT NULL,
-- PRIMARY KEY(stuOutID),
-- FOREIGN KEY(assessID) REFERENCES assessments(assessID)
-- );

-- NOT USED
-- DROP TABLE IF EXISTS `student_learning_objectives`;
-- CREATE TABLE IF NOT EXISTS `student_learning_objectives`(
-- stuLearnObjID INT AUTO_INCREMENT NOT NULL,
-- learnOutID INT NOT NULL,
-- stuOutID INT NOT NULL,
-- PRIMARY KEY(stuLearnObjID),
-- FOREIGN KEY(learnOutID) REFERENCES learning_outcomes(learnOutID),
-- FOREIGN KEY(stuOutID) REFERENCES student_outcomes(stuOutID)
-- );

-- NOT USED
-- DROP TABLE IF EXISTS `chairperson`;
-- CREATE TABLE IF NOT EXISTS `chairperson`(
-- chairID INT AUTO_INCREMENT NOT NULL,
-- firstname VARCHAR(255) NOT NULL,
-- lastname VARCHAR(255) NOT NULL,
-- PRIMARY KEY(chairID)
-- );

-- NOT USED
-- DROP TABLE IF EXISTS `courses`;
-- CREATE TABLE IF NOT EXISTS `courses`(
-- courseID INT AUTO_INCREMENT NOT NULL,
-- name VARCHAR(255) NOT NULL,
-- description CHAR NOT NULL,
-- departmentID INT NOT NULL,
-- PRIMARY KEY(courseID),
-- FOREIGN KEY(departmentID) REFERENCES departments(departmentID)
-- );

-- FOR CLASS RECORD
-- CREATE TABLE IF NOT EXISTS `class_records` (
-- classRecordno INT AUTO_INCREMENT NOT NULL,
-- studentID VARCHAR (10) NOT NULL,
-- lastname VARCHAR(255) NOT NULL,
-- firstname VARCHAR(255) NOT NULL,
-- email VARCHAR(255) NOT NULL,
-- PRIMARY KEY (classRecordno)
-- );

-- USED
DROP TABLE IF EXISTS `assignFaculty`;
CREATE TABLE IF NOT EXISTS `assignFaculty`(
assignFacultyID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
facultyID VARCHAR(10),
subjectID VARCHAR(255),
sectionID VARCHAR(255),
sem VARCHAR(1),
schoolYear VARCHAR(10),
UNIQUE KEY unique_assignFaculty (facultyID, subjectID, sectionID, sem, schoolYear)
);

-- class_record_student untana
DROP TABLE IF EXISTS `students`; 
CREATE TABLE IF NOT EXISTS `students`(
classID INT AUTO_INCREMENT NOT NULL,
classrecordID INT NOT NULL,
studentID VARCHAR(10) NOT NULL,
firstname VARCHAR(255) NOT NULL,
lastname VARCHAR(255) NOT NULL,
courseID VARCHAR(255) NOT NULL,
finalgrade DECIMAL(6,2) NOT NULL DEFAULT 0.00,
email VARCHAR(255) NOT NULL,
PRIMARY KEY (classID),
UNIQUE KEY unique_student (classrecordID, studentID),
FOREIGN KEY(classrecordID) REFERENCES assignFaculty(assignFacultyID)
);

DROP TABLE IF EXISTS `grade_distribution`;
CREATE TABLE IF NOT EXISTS `grade_distribution`(
assessmentID INT AUTO_INCREMENT NOT NULL,
classrecordID INT NOT NULL,
name VARCHAR(255) NOT NULL,
percentage INT NOT NULL,
PRIMARY KEY (assessmentID),
FOREIGN KEY(classrecordID) REFERENCES assignFaculty(assignFacultyID)
);

DROP TABLE IF EXISTS `finalscore`;
CREATE TABLE IF NOT EXISTS `finalscore`(
finalscoreID INT AUTO_INCREMENT NOT NULL,
assessmentID INT NOT NULL,
classID INT NOT NULL,
finalscore DECIMAL(6,2) DEFAULT 0.00,
PRIMARY KEY(finalscoreID),
FOREIGN KEY(assessmentID) REFERENCES grade_distribution(assessmentID) ON DELETE CASCADE,
FOREIGN KEY(classID) REFERENCES students(classID) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `activity`;
CREATE TABLE IF NOT EXISTS `activity` (
activityID INT AUTO_INCREMENT NOT NULL,
assessmentID INT NOT NULL,
classID INT NOT NULL,
scoreLimit DECIMAL(6,2) NOT NULL,
activityName VARCHAR(255) NOT NULL,
score DECIMAL(6,2) DEFAULT 0.00,
PRIMARY KEY (activityID),
UNIQUE KEY unique_activity (assessmentID, classID, activityName),
FOREIGN KEY (assessmentID) REFERENCES grade_distribution(assessmentID) ON DELETE CASCADE,
FOREIGN KEY (classID) REFERENCES students(classID) ON DELETE CASCADE
);

-- USED
DROP TABLE IF EXISTS `faculty`;
CREATE TABLE IF NOT EXISTS `faculty`(
facultyID VARCHAR (10) PRIMARY KEY DEFAULT 'None',
firstname VARCHAR(255) NOT NULL,
lastname VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL,
role ENUM('Chairperson', 'Faculty')
);

-- USED
DROP TABLE IF EXISTS `section`;
CREATE TABLE IF NOT EXISTS `section`(
sectionCode VARCHAR(255) PRIMARY KEY DEFAULT 'None'
);

-- USED
DROP TABLE IF EXISTS `subject`;
CREATE TABLE IF NOT EXISTS `subject`(
subjectID INT AUTO_INCREMENT PRIMARY KEY,
subjectCode VARCHAR(10) NOT NULL,
description VARCHAR(255) NOT NULL,
credits INT,
UNIQUE KEY unique_subject (subjectCode, description, credits)
);

-- USED
DROP TABLE IF EXISTS `subject_section`;
CREATE TABLE IF NOT EXISTS `subject_section`(
subsecID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
subjectID VARCHAR(10),
sectionID VARCHAR(255) DEFAULT 'None',
UNIQUE KEY unique_subject_section (subjectID, sectionID)
);

--  INSERT VALUES SECTION
INSERT INTO `faculty` (facultyID, firstname, lastname, email, role)
VALUES ('None', 'None', 'None', 'None', 'Faculty'),
('2023-0001', 'Fulgent Kvasir', 'Lavesores', 'fulgentkvasir.lavesores@g.msuiit.edu.ph', 'Faculty'),
('2023-0002', 'Alrick Ivan', 'Gicole', 'alrickivan.gicole@g.msuiit.edu.ph', 'Faculty'),
('2023-0003', 'Janella', 'Balantac', 'janellasuzanne.balantac@g.msuiit.edu.ph', 'Faculty'),
('2023-0004', 'Ramel Cary', 'Jamen', 'ramelcary.jamen@g.msuiit.edu.ph', 'Chairperson');

INSERT INTO subject (subjectCode, description, credits)
VALUES
('CCC100', 'Fundamentals of Computing', 3),
('CCC101', 'Computer Programming 1', 3),
('CCC102', 'Computer Programming 2', 3),
('CCC121', 'Data Structures and Algorithm', 3),
('CCC151', 'Information Management', 3),
('CSC112', 'Computer Organization and Architecture', 3),
('CSC124', 'Design and Analysis of Algorithms', 3),
('CSC186', 'Human-Computer Interaction', 3),
('CCC181', 'Applications Development and Emerging Technologies', 3),
('CSC145', 'Programming Languages', 3);

INSERT INTO section (sectionCode)
VALUES
('None'),
('CS1A'),
('CS1B'),
('CS1C'),
('CS2A'),
('CS2B'),
('CS2C'),
('CS3A'),
('CS3B'),
('CS3C'),
('CS4A'),
('CS4B'),
('CS4C');

INSERT INTO subject_section (subjectID, sectionID)
VALUES
('CCC100', 'CS1C'),
('CCC101', 'CS2B'),
('CCC102', 'CS1A'),
('CCC121', 'CS1A'),
('CCC151', 'CS4B'),
('CSC112', 'CS4B'),
('CSC124', 'CS4C'),
('CSC186', 'CS4C'),
('CCC181', 'CS2B'),
('CSC145', 'CS4C');

INSERT INTO assignFaculty (facultyID, subjectID, sectionID, sem, schoolYear)
VALUES
('None', 'CCC100', 'CS1C', '1', '2023-2024'),
('None', 'CCC101', 'CS2B', '1', '2023-2024'),
('None', 'CCC102', 'CS1A', '1', '2023-2024'),
('None', 'CCC121', 'CS1A', '1', '2023-2024'),
('None', 'CCC151', 'CS4B', '1', '2023-2024'),
('None', 'CSC112', 'CS4B', '1', '2023-2024'),
('None', 'CSC124', 'CS4C', '1', '2023-2024'),
('None', 'CSC186', 'CS4C', '1', '2023-2024'),
('None', 'CCC181', 'CS2B', '1', '2023-2024'),
('None', 'CSC145', 'CS4C', '1', '2023-2024');
