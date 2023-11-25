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

DROP TABLE IF EXISTS `faculty`;
CREATE TABLE IF NOT EXISTS `faculty`(
facultyID VARCHAR (10) PRIMARY KEY DEFAULT 'None',
firstname VARCHAR(255) NOT NULL,
lastname VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS `section`;
CREATE TABLE IF NOT EXISTS `section`(
sectionCode VARCHAR(255) PRIMARY KEY
);

DROP TABLE IF EXISTS `subject`;
CREATE TABLE IF NOT EXISTS `subject`(
subjectID INT AUTO_INCREMENT PRIMARY KEY,
subjectCode VARCHAR(10) NOT NULL,
description VARCHAR(255) NOT NULL,
credits INT,
UNIQUE KEY unique_subject (subjectCode, description, credits)
);

-- Drop the existing schedule table if it exists

DROP TABLE IF EXISTS `subject_section`;
CREATE TABLE IF NOT EXISTS `subject_section`(
subsecID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
subjectID VARCHAR(10),
sectionID VARCHAR(255),
UNIQUE KEY unique_subject_section (subjectID, sectionID)
);

DROP TABLE IF EXISTS `schedule`;

CREATE TABLE IF NOT EXISTS `schedule` (
    scheduleID INT PRIMARY KEY AUTO_INCREMENT,
    subjectID VARCHAR(10),
    sectionID VARCHAR(255),
    day VARCHAR(255),
    time_start TIME,
    time_end TIME,
    CONSTRAINT unique_schedule_time UNIQUE (day, time_start, time_end),
    FOREIGN KEY (subjectID, sectionID) REFERENCES subject_section(subjectID, sectionID)
);



-- to handle 1 section of the same subject
-- but can handle many subjects (subjectID not unique) of the same section-- Drop the existing assignFaculty table if it exists
DROP TABLE IF EXISTS `assignFaculty`;
CREATE TABLE IF NOT EXISTS `assignFaculty`(
assignFacultyID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
facultyID VARCHAR(10),
subjectID VARCHAR(255),
sectionID VARCHAR(255),
UNIQUE KEY unique_assignFaculty (facultyID, subjectID, sectionID)
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

INSERT INTO `faculty` (facultyID, firstname ,lastname, email)
VALUES ('None', 'None', 'None', 'None');

INSERT INTO `faculty` (facultyID, firstname, lastname, email)
VALUES ('2023-0001', 'Fulgent', 'Lavesores', 'fulgent.lavesores@g.msuiit.edu.ph'),
('2023-0002', 'Alrick', 'Gicole', 'alrick.gicole@g.msuiit.edu.ph'),
('2023-0003', 'Janella', 'Balantac', 'janella.balantac@g.msuiit.edu.ph'),
('2023-0004', 'Ramel Cary', 'Jamen', 'ramelcary.jamen@g.msuiit.edu.ph');

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
('CCC181', 'Applications Development and
Emerging Technologies', 3),
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

-- First, insert data into subject_section
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

-- Then, insert data into the schedule table
INSERT INTO assignFaculty (facultyID, subjectID, sectionID)
VALUES
('None', 'CCC100', 'CS1C'),
('None', 'CCC101', 'CS2B'),
('None', 'CCC102', 'CS1A'),
('None', 'CCC121', 'CS1A'),
('None', 'CCC151', 'CS4B'),
('None', 'CSC112', 'CS4B'),
('None', 'CSC124', 'CS4C'),
('None', 'CSC186', 'CS4C'),
('None', 'CCC181', 'CS2B'),
('None', 'CSC145', 'CS4C');


-- Insert data into the schedule table
-- INSERT INTO `schedule` (subjectID, sectionID, day, time_start, time_end)
-- VALUES 
-- ('CCC100', 'CS1C', 'Monday', '09:00', '10:30'),
-- ('CCC101', 'CS2B', 'Tuesday', '10:30', '12:00'),
-- ('CCC102', 'CS1A', 'Wednesday', '13:00', '14:30'),
-- ('CCC121', 'CS1A', 'Thursday', '15:00', '16:30'),
-- ('CCC151', 'CS4B', 'Friday', '14:00', '15:30'),
-- ('CSC112', 'CS4B', 'Monday', '09:00', '10:30'),
-- ('CSC124', 'CS4C', 'Tuesday', '10:30', '12:00'),
-- ('CSC186', 'CS4C', 'Wednesday', '13:00', '14:30'),
-- ('CCC181', 'CS2B', 'Thursday', '15:00', '16:30'),
-- ('CSC145', 'CS4C', 'Friday', '14:00', '15:30');


