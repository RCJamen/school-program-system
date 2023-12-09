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
                finalgrade DECIMAL(6,2) NOT NULL DEFAULT 0.00,
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

    @classmethod
    def deleteStudent(cls, subject_code, section_code, school_year, sem, studentID):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'CR_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')

            # Delete the row
            cursor.execute(f"DELETE FROM {table_name} WHERE studentID = %s", (studentID,))
            mysql.connection.commit()

            # Reorder the classID values to ensure sequential order
            cursor.execute(f"SET @new_classID := 0;")
            cursor.execute(f"UPDATE {table_name} SET classID = @new_classID := @new_classID + 1 ORDER BY classID;")
            mysql.connection.commit()

            return "Student deleted successfully"
        except Exception as e:
            return f"Failed to delete student: {str(e)}"
