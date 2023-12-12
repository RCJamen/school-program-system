from app import mysql
from decimal import Decimal

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
            cr_table_name = f'CR_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
            cursor.execute(f"DELETE FROM {cr_table_name} WHERE studentID = %s", (studentID,))
            mysql.connection.commit()

            cursor.execute(f"SET @new_classID := 0;")
            cursor.execute(f"UPDATE {cr_table_name} SET classID = @new_classID := @new_classID + 1 ORDER BY classID;")
            mysql.connection.commit()

            cursor.execute(f"SELECT MAX(classID) AS max_classID FROM {cr_table_name};")
            max_classID = cursor.fetchone()[0]
            max_classID += 1

            cursor.execute(f"ALTER TABLE {cr_table_name} AUTO_INCREMENT = {max_classID};")
            mysql.connection.commit()

            as_table_name = f'AS_{subject_code}_{section_code}_{school_year}_{sem}%'.replace('-', '_')
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE %s AND table_schema = 'progsys_db'", (as_table_name,))
            as_tables = cursor.fetchall()

            for table in as_tables:
                as_table_name = table[0]
                cursor.execute(f"DELETE FROM {as_table_name} WHERE studentID = %s", (studentID,))
                mysql.connection.commit()

                cursor.execute(f"SET @new_classID := 0;")
                cursor.execute(f"UPDATE {as_table_name} SET classID = @new_classID := @new_classID + 1 ORDER BY classID;")
                mysql.connection.commit()

                cursor.execute(f"SELECT MAX(classID) AS max_classID FROM {as_table_name};")
                max_classID = cursor.fetchone()[0]
                max_classID += 1
                cursor.execute(f"ALTER TABLE {as_table_name} AUTO_INCREMENT = {max_classID};")
                mysql.connection.commit()

            return "Student deleted successfully"
        except Exception as e:
            return f"Failed to delete student: {str(e)}"

    @staticmethod
    def createGradeDistributionTable(subject_code, section_code, school_year, sem):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'GD_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
            sql = '''
                CREATE TABLE IF NOT EXISTS {} (
                assessmentID INT AUTO_INCREMENT NOT NULL,
                name VARCHAR(255) NOT NULL,
                percentage INT NOT NULL,
                PRIMARY KEY (assessmentID),
                UNIQUE KEY (name)
                );
            '''.format(table_name)
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except Exception as e:
            return f"Failed to Create Database: {str(e)}"

    @staticmethod
    def getGradeDistribution(subject_code, section_code, school_year, sem):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'GD_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
            sql = f"SELECT * FROM {table_name}"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return f"Failed to fetch students: {str(e)}"

    @staticmethod
    def addGradeDistribution(subject_code, section_code, school_year, sem, name, percentage):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'GD_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
            check_query = f"SELECT COALESCE(SUM(percentage), 0) FROM {table_name}"
            cursor.execute(check_query)
            total_percentage = Decimal(cursor.fetchone()[0])
            percentage = Decimal(str(percentage))
            if total_percentage + percentage > 100:
                return "Sum of percentage values cannot exceed 100"
            insert_query = f"INSERT INTO {table_name} (name, percentage) VALUES (%s, %s)"
            values = (name, percentage)
            cursor.execute(insert_query, values)
            mysql.connection.commit()
            return "Assessment created successfully"
        except Exception as e:
            return f"{str(e)}"

    @classmethod
    def deleteGradeAssessment(cls, subject_code, section_code, school_year, sem, assessmentid):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'GD_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')

            # Delete the row
            cursor.execute(f"DELETE FROM {table_name} WHERE assessmentID = %s", (assessmentid,))
            mysql.connection.commit()

            # Reorder the assessmentID values to ensure sequential order
            cursor.execute(f"SET @new_assessmentID := 0;")
            cursor.execute(f"UPDATE {table_name} SET assessmentID = @new_assessmentID := @new_assessmentID + 1 ORDER BY assessmentid;")
            mysql.connection.commit()

            return "Assessment deleted successfully"
        except Exception as e:
            return f"Failed to delete assessment: {str(e)}"

    @staticmethod
    def getRowsClassRecord(subject_code, section_code, school_year, sem):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'CR_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
            sql = f"SELECT classID, studentID, firstname, lastname, email FROM {table_name}"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return f"Failed to fetch students: {str(e)}"

    @staticmethod
    def createAssessmentTable(subject_code, section_code, school_year, sem, name, rows):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'AS_{subject_code}_{section_code}_{school_year}_{sem}_{name.replace(" ", "_")}'.replace('-', '_')

            create_table_sql = '''
                CREATE TABLE IF NOT EXISTS {} (
                classID INT AUTO_INCREMENT,
                studentID VARCHAR(20),
                firstname VARCHAR(255),
                lastname VARCHAR(255),
                email VARCHAR(255),
                finalscore DECIMAL(6,2) DEFAULT 0.00,
                Activity_1 INT DEFAULT 0,
                PRIMARY KEY (classID)
                );
            '''.format(table_name)
            cursor.execute(create_table_sql)

            for row in rows:
                classID = row[0]
                studentID = row[1]
                firstname = row[2]
                lastname = row[3]
                email = row[4]
                insert_row_sql = f"INSERT INTO {table_name} (classID, studentID, firstname, lastname, email) VALUES ({classID},'{studentID}', '{firstname}', '{lastname}', '{email}')"
                cursor.execute(insert_row_sql)

            mysql.connection.commit()
            return True
        except Exception as e:
            return f"Failed to Create Assessment Table: {str(e)}"


    @staticmethod
    def deleteAssessmentTable(subject_code, section_code, school_year, sem, name):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'AS_{subject_code}_{section_code}_{school_year}_{sem}_{name.replace(" ", "_")}'.replace('-', '_')
            sql = '''
                DROP TABLE {};
                '''.format(table_name)
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except Exception as e:
            return f"Failed to Delete Database Table: {str(e)}"


    @staticmethod
    def getAssessmentList(subject_code, section_code, school_year, sem):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'GD_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
            sql = f"SELECT name FROM {table_name} ORDER BY assessmentID"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return f"Failed to fetch Assessments: {str(e)}"


    @staticmethod
    def getStudentsInAssessment(subject_code, section_code, school_year, sem, assessment):
        try:
            cursor = mysql.connection.cursor()
            table_name = f'AS_{subject_code}_{section_code}_{school_year}_{sem}_{assessment}'.replace('-', '_')
            sql = f"SELECT * FROM {table_name}"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return f"Failed to fetch Students in Assessments: {str(e)}"
