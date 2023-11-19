    DROP DATABASE IF EXISTS `progsys_db`;
CREATE DATABASE IF NOT EXISTS `progsys_db`;
use `progsys_db`;


DROP TABLE IF EXISTS `colleges`;
CREATE TABLE IF NOT EXISTS `colleges`(
collegeID INT AUTO_INCREMENT NOT NULL,
name VARCHAR(255) NOT NULL,
PRIMARY KEY(collegeID)
);

DROP TABLE IF EXISTS `curriculum`;
CREATE TABLE IF NOT EXISTS `curriculum`(
currID INT AUTO_INCREMENT NOT NULL,
name VARCHAR(255) NOT NULL,
description CHAR NOT NULL,
PRIMARY KEY(currID)
);

DROP TABLE IF EXISTS `departments`;
CREATE TABLE IF NOT EXISTS `departments`(
departmentID INT AUTO_INCREMENT NOT NULL,
name VARCHAR(255) NOT NULL,
collegeID INT NOT NULL,
currID INT NOT NULL,
PRIMARY KEY(departmentID),
FOREIGN KEY(collegeID) REFERENCES colleges(collegeID),
FOREIGN KEY(currID) REFERENCES curriculum(currID)
);

DROP TABLE IF EXISTS `learning_outcomes`;
CREATE TABLE IF NOT EXISTS `learning_outcomes`(
learnOutID INT AUTO_INCREMENT NOT NULL,
title VARCHAR(255) NOT NULL,
description CHAR NOT NULL,
currID INT NOT NULL,
PRIMARY KEY(learnOutID),
FOREIGN KEY(currID) REFERENCES curriculum(currID)
);

DROP TABLE IF EXISTS `assessments`;
CREATE TABLE IF NOT EXISTS `assessments`(
assessID INT AUTO_INCREMENT NOT NULL,
name VARCHAR(255) NOT NULL,
score INT NOT NULL,
totalScore INT NOT NULL,
PRIMARY KEY(assessID)
);

DROP TABLE IF EXISTS `student_outcomes`;
CREATE TABLE IF NOT EXISTS `student_outcomes`(
stuOutID INT AUTO_INCREMENT NOT NULL,
name VARCHAR(255) NOT NULL,
description CHAR NOT NULL,
assessID INT NOT NULL,
PRIMARY KEY(stuOutID),
FOREIGN KEY(assessID) REFERENCES assessments(assessID)
);

DROP TABLE IF EXISTS `student_learning_objectives`;
CREATE TABLE IF NOT EXISTS `student_learning_objectives`(
stuLearnObjID INT AUTO_INCREMENT NOT NULL,
learnOutID INT NOT NULL,
stuOutID INT NOT NULL,
PRIMARY KEY(stuLearnObjID),
FOREIGN KEY(learnOutID) REFERENCES learning_outcomes(learnOutID),
FOREIGN KEY(stuOutID) REFERENCES student_outcomes(stuOutID)
);

DROP TABLE IF EXISTS `courses`;
CREATE TABLE IF NOT EXISTS `courses`(
courseID INT AUTO_INCREMENT NOT NULL,
name VARCHAR(255) NOT NULL,
description CHAR NOT NULL,
departmentID INT NOT NULL,
PRIMARY KEY(courseID),
FOREIGN KEY(departmentID) REFERENCES departments(departmentID)
);

DROP TABLE IF EXISTS `chairperson`;
CREATE TABLE IF NOT EXISTS `chairperson`(
chairID INT AUTO_INCREMENT NOT NULL,
firstname VARCHAR(255) NOT NULL,
lastname VARCHAR(255) NOT NULL,
PRIMARY KEY(chairID)
);

DROP TABLE IF EXISTS `faculty`;
CREATE TABLE IF NOT EXISTS `faculty`(
facultyID VARCHAR (9) NOT NULL,
firstname VARCHAR(255) NOT NULL,
lastname VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL,
PRIMARY KEY(facultyID)
);

DROP TABLE IF EXISTS `students`;
CREATE TABLE IF NOT EXISTS `students`(
studentID INT AUTO_INCREMENT NOT NULL,
firstname VARCHAR(255) NOT NULL,
lastname VARCHAR(255) NOT NULL,
courseID INT NOT NULL,
gmail VARCHAR(255) NOT NULL,
PRIMARY KEY(studentID),
FOREIGN KEY(courseID) REFERENCES courses(courseID)
);

DROP TABLE IF EXISTS `section`;
CREATE TABLE IF NOT EXISTS `section`(
sectionCode VARCHAR(255) PRIMARY KEY
);

DROP TABLE IF EXISTS `subject`;
CREATE TABLE IF NOT EXISTS `subject`(
subjectCode VARCHAR(255) PRIMARY KEY NOT NULL UNIQUE,
description VARCHAR(255) NOT NULL,
credits INT,
semester INT
);

DROP TABLE IF EXISTS `subject_section`;
CREATE TABLE IF NOT EXISTS `subject_section`(
subjectID VARCHAR(9),
sectionID VARCHAR(255),
PRIMARY KEY (subjectID, sectionID),
FOREIGN KEY (subjectID) REFERENCES subject(subjectCode),
FOREIGN KEY (sectionID) REFERENCES section(sectionCode)
);


-- to handle 1 section of the same subject
-- but can handle many subjects (subjectID not unique) of the same section-- Drop the existing assignFaculty table if it exists
DROP TABLE IF EXISTS `assignFaculty`;

-- Create the assignFaculty table with foreign key constraints
CREATE TABLE IF NOT EXISTS `assignFaculty`(
    facultyID VARCHAR(9),
    subjectID VARCHAR(255),
    sectionID VARCHAR(255),
    PRIMARY KEY (subjectID, sectionID),  -- Change the primary key
    FOREIGN KEY (facultyID) REFERENCES faculty(facultyID) ON DELETE SET NULL,
    FOREIGN KEY (subjectID) REFERENCES subject(subjectCode) ON DELETE CASCADE,
    FOREIGN KEY (sectionID) REFERENCES section(sectionCode) ON DELETE CASCADE
);



DROP TABLE IF EXISTS `class_records`;
CREATE TABLE IF NOT EXISTS `class_records`(
classRecordID INT AUTO_INCREMENT NOT NULL,
studentID INT NOT NULL,
subjectCode VARCHAR(255) NOT NULL,
assessID INT NOT NULL,
totalGrade INT NOT NULL,
PRIMARY KEY(classRecordID),
FOREIGN KEY(studentID) REFERENCES students(studentID),
FOREIGN KEY(subjectCode) REFERENCES subject(subjectCode),
FOREIGN KEY(assessID) REFERENCES assessments(assessID)
);

INSERT INTO `faculty` (facultyID, firstname, lastname, email)
VALUES ('2023-0001', 'Fulgent', 'Travesores', 'fulgent.travesores@g.msuiit.edu.ph'),
('2023-0002', 'Alrick', 'Gicole', 'alrick.gicole@g.msuiit.edu.ph'),
('2023-0003', 'Janella', 'Balantac', 'janella.balantac@g.msuiit.edu.ph'),
('2023-0004', 'Ramel Cary', 'Jamen', 'ramelcary.jamen@g.msuiit.edu.ph');

INSERT INTO subject (subjectCode, description, credits, semester)
VALUES 
('CCC181', 'Application Development', 3, 1),
('CSC181', 'Software Engineering', 3, 2),
('CSC173', 'Intelligent Systems', 3, 1),
('CCC102', 'Computer Programming II', 3, 2);

INSERT INTO section (sectionCode)
VALUES
('CS1'),
('CS2'),
('CS3A'),
('CS3B'),
('CS4');

INSERT INTO subject_section (subjectID, sectionID)
VALUES
('CCC102', 'CS2'),
('CCC181', 'CS3A'),
('CCC181', 'CS3B'),
('CSC181', 'CS3A'),
('CSC181', 'CS3B');

INSERT INTO assignFaculty (facultyID, subjectID, sectionID)
VALUES
('2023-0001', 'CSC181', 'CS3A'),
('2023-0001', 'CCC181', 'CS3A'),
('2023-0002', 'CSC181', 'CS3B'),
('2023-0002', 'CCC181', 'CS3B'),
('2023-0004', 'CCC102', 'CS2');
