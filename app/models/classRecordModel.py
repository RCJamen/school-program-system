from app import mysql

class ClassRecord:

    @staticmethod
    def createClassRecordTable(subject_code, section_code, school_year, sem):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'CR_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
            sql = '''
                CREATE TABLE IF NOT EXISTS {} (
                classID INT AUTO_INCREMENT NOT NULL,
                studentID VARCHAR(10) NOT NULL,
                firstname VARCHAR(255) NOT NULL,
                lastname VARCHAR(255) NOT NULL,
                courseID VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                PRIMARY KEY (classID),
                UNIQUE KEY (studentID)
                );
            '''.format(table_name)
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except Exception as e:
            return f"Failed to Create Database: {str(e)}"

    @staticmethod
    def getStudents(subject_code, section_code, school_year, sem):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'CR_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
            sql = f"SELECT * FROM {table_name}"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return f"Failed to fetch students: {str(e)}"

    @staticmethod
    def addStudent(subject_code, section_code, school_year, sem, studentID, firstname, lastname, coursecode, email):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'CR_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
            insert_query = f"INSERT INTO {table_name} (studentID, firstname, lastname, courseID, email) VALUES (%s, %s, %s, %s, %s)"
            values = (studentID, firstname, lastname, coursecode, email)
            cursor.execute(insert_query, values)
            mysql.connection.commit()
            return "Student created successfully"
        except Exception as e:
            return f"Failed to create Student: {str(e)}"
