from app import mysql
import csv
from decimal import Decimal
class ClassRecord:

    @classmethod
    def getClassRecordData(cls, classrecordid):
        try:
            cursor = mysql.connection.cursor()
            sql = '''SELECT
                        s.subjectCode,
                        af.sectionID,
                        s.description,
                        s.credits,
                        af.sem,
                        af.schoolYear
                    FROM
                        assignFaculty AS af
                    LEFT JOIN
                        subject AS s ON af.subjectID = s.subjectCode
                    LEFT JOIN
                        faculty AS f ON af.facultyID = f.facultyID
                    WHERE
                        af.assignFacultyID = %s'''
            cursor.execute(sql, (classrecordid,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            return f"Failed to load details for AssignFacultyID: {str(e)}"

    @staticmethod
    def getClassRecordStudents(classrecordid):
        try:
            cursor = mysql.connection.cursor()
            sql = 'SELECT classrecordID, classID, studentID, firstname, lastname, courseID, finalgrade, email FROM students WHERE classrecordID = %s ORDER BY classID'
            cursor.execute(sql,(classrecordid,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return f"Failed to fetch students: {str(e)}"

    @staticmethod
    def getstudentclassID(classrecordid, studentID):
        try:
            cursor = mysql.connection.cursor()
            sql = 'SELECT classID FROM students WHERE classrecordID = %s AND studentID = %s'
            cursor.execute(sql,(classrecordid, studentID))
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        except Exception as e:
            return f"Failed to fetch students: {str(e)}"

    @staticmethod
    def postStudentToClassRecord(classrecordid, studentID, firstname, lastname, coursecode, email):
        try:
            cursor = mysql.connection.cursor()
            sql = 'INSERT INTO students (classrecordID, studentID, firstname, lastname, courseID, email) VALUES (%s, %s, %s, %s, %s, %s)'
            cursor.execute(sql,(classrecordid,studentID,firstname,lastname,coursecode,email,))
            cursor.close()
            mysql.connection.commit()
            return "Student Created Successfully"
        except Exception as e:
            return f"Failed to create Student: {str(e)}"

    @staticmethod
    def deleteStudentFromClassRecord(classrecordid, studentID, classID):
        try:
            cursor = mysql.connection.cursor()
            sql = 'DELETE FROM activity WHERE classID = %s'
            cursor.execute(sql,(classID,))
            mysql.connection.commit()
            sql = 'DELETE FROM students WHERE classrecordID = %s AND studentID = %s'
            cursor.execute(sql,(classrecordid, studentID,))
            mysql.connection.commit()
            cursor.close()
            return "Student deleted successfully"
        except Exception as e:
            return f"Failed to Delete Student: {str(e)}"


    @staticmethod
    def getGradeDistribution(classrecordid):
        try:
            cursor = mysql.connection.cursor()
            sql = 'SELECT assessmentID, name, percentage FROM grade_distribution WHERE classrecordID = %s ORDER BY assessmentID'
            cursor.execute(sql,(classrecordid,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            return f"Failed to fetch assessments: {str(e)}"

    @staticmethod
    def postGradeDistribution(classrecordid, name, percentage):
        try:
            cursor = mysql.connection.cursor()
            check_query = 'SELECT COALESCE(SUM(percentage), 0) FROM grade_distribution WHERE classrecordID = %s'
            cursor.execute(check_query,(classrecordid,))
            total_percentage = Decimal(cursor.fetchone()[0])
            percentage = Decimal(str(percentage))
            if total_percentage + percentage > 100:
                return "Sum of percentage values cannot exceed 100"
            insert_query = 'INSERT INTO grade_distribution (classrecordID, name, percentage) VALUES (%s, %s, %s)'
            cursor.execute(insert_query, (classrecordid, name, percentage,))
            mysql.connection.commit()
            return "Assessment created successfully"
        except Exception as e:
            return f"{str(e)}"

    @classmethod
    def deleteGradeDistribution(cls, classrecordid, assessmentname):
        try:
            cursor = mysql.connection.cursor()
            sql = 'DELETE FROM grade_distribution WHERE classrecordID = %s AND name = %s'
            cursor.execute(sql, (classrecordid, assessmentname,))
            mysql.connection.commit()
            cursor.close()
            return "Assessment deleted successfully"
        except Exception as e:
            return f"Failed to Delete Assessment: {str(e)}"

    @staticmethod
    def getAssessmentID(classrecordid, name):
        try:
            cursor = mysql.connection.cursor()
            sql = 'SELECT assessmentID FROM grade_distribution WHERE classrecordID = %s AND name = %s'
            cursor.execute(sql,(classrecordid, name,))
            result = cursor.fetchone()[0]
            cursor.close()
            return result
        except Exception as e:
            return f"Failed to get assessmentID: {str(e)}"

    @staticmethod
    def postCreateActivity(asessmentID, studentsID):
        try:
            cursor = mysql.connection.cursor()
            for student in studentsID:
                sql = 'INSERT INTO activity (assessmentID, classID) VALUES (%s, %s)'
                cursor.execute(sql,(asessmentID, student))
            mysql.connection.commit()
            return "Student Inserted in Activity Successfully"
        except Exception as e:
            return f"Failed to insert students to Activity: {str(e)}"


    csv_data = None
    @classmethod
    def upload_csv(cls, file, classrecordid):
        try:
            if file and file.filename.endswith('.csv'):
                cls.load_csv_data(file)
                cursor = mysql.connection.cursor()
                for index, row in enumerate(cls.csv_data):
                    if index == 0:
                        continue

                    insert_query = f"INSERT INTO students (classrecordID, studentID, firstname, lastname, courseID, email) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (classrecordid, row[0], row[1], row[2], row[3], row[4])
                    cursor.execute(insert_query, values)

                mysql.connection.commit()
                return {"type": "success", "message": 'File uploaded and data inserted successfully.'}
            else:
                return {"type": "danger", "message": 'Invalid file format. Please upload a CSV file.'}
        except Exception as e:
            error_message = f'Error: {str(e)}'
            return {"type": "danger", "message": error_message}

    @classmethod
    def truncate_classrecord (cls, classrecordid):
        try:
            cursor = mysql.connection.cursor()
            sql = 'DELETE FROM students WHERE classrecordID = %s'
            cursor.execute(sql, (classrecordid,))
            mysql.connection.commit()
            return "Classrecord truncated successfully"
        except Exception as e:
            return f"Error: {str(e)}"

    @classmethod
    def load_csv_data(cls, file):
        if cls.csv_data is None:
            cls.csv_data = None
        file_content = file.read().decode('utf-8').splitlines()
        cls.csv_data = list(csv.reader(file_content))

    @staticmethod
    def getFinalScores(assessmentIDs):
        try:
            cursor = mysql.connection.cursor()
            sql = """
                SELECT finalscore
                FROM activity
                WHERE assessmentID IN {}
                ORDER BY assessmentID, classID
            """.format(tuple(assessmentIDs))

            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()

            return results
        except Exception as e:
            return f"Failed to fetch assessments: {str(e)}"





















    # @staticmethod
    # def createAssessmentTable(subject_code, section_code, school_year, sem, name, rows):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'AS_{subject_code}_{section_code}_{school_year}_{sem}_{name.replace(" ", "_")}'.replace('-', '_')

    #         create_table_sql = '''
    #             CREATE TABLE IF NOT EXISTS {} (
    #             classID INT AUTO_INCREMENT,
    #             studentID VARCHAR(20),
    #             firstname VARCHAR(255),
    #             lastname VARCHAR(255),
    #             email VARCHAR(255),
    #             finalscore DECIMAL(6,2) DEFAULT 0.00,
    #             PRIMARY KEY (classID)
    #             );
    #         '''.format(table_name)
    #         cursor.execute(create_table_sql)

    #         for row in rows:
    #             classID = row[0]
    #             studentID = row[1]
    #             firstname = row[2]
    #             lastname = row[3]
    #             email = row[4]
    #             insert_row_sql = f"INSERT INTO {table_name} (classID, studentID, firstname, lastname, email) VALUES ({classID},'{studentID}', '{firstname}', '{lastname}', '{email}')"
    #             cursor.execute(insert_row_sql)

    #         mysql.connection.commit()
    #         return True
    #     except Exception as e:
    #         return f"Failed to Create Assessment Table: {str(e)}"


    # @staticmethod
    # def deleteAssessmentTable(subject_code, section_code, school_year, sem, name):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'AS_{subject_code}_{section_code}_{school_year}_{sem}_{name.replace(" ", "_")}'.replace('-', '_')
    #         sql = '''
    #             DROP TABLE {};
    #             '''.format(table_name)
    #         cursor.execute(sql)
    #         mysql.connection.commit()
    #         return True
    #     except Exception as e:
    #         return f"Failed to Delete Database Table: {str(e)}"


    # @staticmethod
    # def getAssessmentList(subject_code, section_code, school_year, sem):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'GD_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
    #         sql = f"SELECT name, percentage FROM {table_name} ORDER BY assessmentID"
    #         cursor.execute(sql)
    #         result = cursor.fetchall()
    #         cursor.close()
    #         return result
    #     except Exception as e:
    #         return f"Failed to fetch Assessments: {str(e)}"

    # @staticmethod
    # def getStudentsInAssessment(subject_code, section_code, school_year, sem, assessment):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'AS_{subject_code}_{section_code}_{school_year}_{sem}_{assessment}'.replace('-', '_')
    #         sql = f"SELECT * FROM {table_name}"
    #         cursor.execute(sql)
    #         result = cursor.fetchall()
    #         cursor.close()
    #         return result
    #     except Exception as e:
    #         return f"Failed to fetch Students in Assessments: {str(e)}"

    # @staticmethod
    # def getAssessmentColumns(subject_code, section_code, school_year, sem, assessment):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'AS_{subject_code}_{section_code}_{school_year}_{sem}_{assessment}'.replace('-', '_')
    #         sql = f"SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position";
    #         cursor.execute(sql)
    #         result = cursor.fetchall()
    #         cursor.close()
    #         return result
    #     except Exception as e:
    #         return f"Failed to fetch Tables in Assessment: {str(e)}"

    # @staticmethod
    # def addAssessmentActivity(subject_code, section_code, school_year, sem, assessment, name, scorelimit):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'AS_{subject_code}_{section_code}_{school_year}_{sem}_{assessment}'.replace('-', '_')
    #         column_name = f'{name}_{scorelimit}'
    #         sql = '''
    #             ALTER TABLE {} ADD {} INT DEFAULT 0 CHECK ({} >= 0 AND {} <= {});
    #             '''.format(table_name, column_name, column_name, column_name, scorelimit)
    #         cursor.execute(sql)
    #         mysql.connection.commit()
    #         return "Activity created successfully"
    #     except Exception as e:
    #         return f"{str(e)}"




    # @staticmethod
    # def createClassRecordTable(subject_code, section_code, school_year, sem):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'CR_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
    #         sql = '''
    #             CREATE TABLE IF NOT EXISTS {} (
    #             classID INT AUTO_INCREMENT NOT NULL,
    #             studentID VARCHAR(10) NOT NULL,
    #             firstname VARCHAR(255) NOT NULL,
    #             lastname VARCHAR(255) NOT NULL,
    #             courseID VARCHAR(255) NOT NULL,
    #             finalgrade DECIMAL(6,2) NOT NULL DEFAULT 0.00,
    #             email VARCHAR(255) NOT NULL,
    #             PRIMARY KEY (classID),
    #             UNIQUE KEY (studentID)
    #             );
    #         '''.format(table_name)
    #         cursor.execute(sql)
    #         mysql.connection.commit()
    #         return True
    #     except Exception as e:
    #         return f"Failed to Create Database: {str(e)}"


    # @staticmethod
# def getStudents(subject_code, section_code, school_year, sem):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'CR_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
    #         sql = f"SELECT * FROM {table_name}"
    #         cursor.execute(sql)
    #         result = cursor.fetchall()
    #         cursor.close()
    #         return result
    #     except Exception as e:
    #         return f"Failed to fetch students: {str(e)}"


    # @staticmethod
    # def addStudent(subject_code, section_code, school_year, sem, studentID, firstname, lastname, coursecode, email):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'CR_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
    #         insert_query = f"INSERT INTO {table_name} (studentID, firstname, lastname, courseID, email) VALUES (%s, %s, %s, %s, %s)"
    #         values = (studentID, firstname, lastname, coursecode, email)
    #         cursor.execute(insert_query, values)
    #         mysql.connection.commit()

    #         as_table_name = f'AS_{subject_code}_{section_code}_{school_year}_{sem}%'.replace('-', '_')
    #         cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE %s AND table_schema = 'progsys_db'", (as_table_name,))
    #         as_tables = cursor.fetchall()

    #         for table in as_tables:
    #             as_table_name = table[0]
    #             cursor.execute(f"INSERT INTO {as_table_name} (studentID, firstname, lastname, email) VALUES (%s, %s, %s, %s)", (studentID, firstname, lastname, email))
    #             mysql.connection.commit()

    #         return "Student created successfully"
    #     except Exception as e:
    #         return f"Failed to create Student: {str(e)}"



    # @classmethod
    # def deleteStudent(cls,subject_code, section_code, school_year, sem, studentID):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         cr_table_name = f'CR_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')

    #         cursor.execute(f"DELETE FROM {cr_table_name} WHERE studentID = %s", (studentID,))
    #         mysql.connection.commit()

    #         cursor.execute(f"SET @new_classID := 0;")
    #         cursor.execute(f"UPDATE {cr_table_name} SET classID = @new_classID := @new_classID + 1 ORDER BY classID;")
    #         mysql.connection.commit()

    #         cursor.execute(f"SELECT MAX(classID) AS max_classID FROM {cr_table_name};")
    #         max_classID_result = cursor.fetchone()
    #         max_classID = max_classID_result[0] + 1 if max_classID_result[0] is not None else 1

    #         cursor.execute(f"ALTER TABLE {cr_table_name} AUTO_INCREMENT = {max_classID};")
    #         mysql.connection.commit()

    #         as_table_name = f'AS_{subject_code}_{section_code}_{school_year}_{sem}%'.replace('-', '_')
    #         cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name LIKE %s AND table_schema = 'progsys_db'", (as_table_name,))
    #         as_tables = cursor.fetchall()

    #         for table in as_tables:
    #             as_table_name = table[0]
    #             cursor.execute(f"DELETE FROM {as_table_name} WHERE studentID = %s", (studentID,))
    #             mysql.connection.commit()

    #             cursor.execute(f"SET @new_classID := 0;")
    #             cursor.execute(f"UPDATE {as_table_name} SET classID = @new_classID := @new_classID + 1 ORDER BY classID;")
    #             mysql.connection.commit()

    #             cursor.execute(f"SELECT MAX(classID) AS max_classID FROM {as_table_name};")
    #             max_classID_result = cursor.fetchone()
    #             max_classID = max_classID_result[0] + 1 if max_classID_result[0] is not None else 1

    #             cursor.execute(f"ALTER TABLE {as_table_name} AUTO_INCREMENT = {max_classID};")
    #             mysql.connection.commit()
    #         return "Student deleted successfully"
    #     except Exception as e:
    #         return f"Failed to delete student: {str(e)}"
    #         return f"Failed to delete student: {str(e)}"

# @staticmethod
    # def createGradeDistributionTable(subject_code, section_code, school_year, sem):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'GD_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
    #         sql = '''
    #             CREATE TABLE IF NOT EXISTS {} (
    #             assessmentID INT AUTO_INCREMENT NOT NULL,
    #             name VARCHAR(255) NOT NULL,
    #             percentage INT NOT NULL,
    #             PRIMARY KEY (assessmentID),
    #             UNIQUE KEY (name)
    #             );
    #         '''.format(table_name)
    #         cursor.execute(sql)
    #         mysql.connection.commit()
    #         return True
    #     except Exception as e:
    #         return f"Failed to Create Database: {str(e)}"


    # @staticmethod
    # def addGradeDistribution(subject_code, section_code, school_year, sem, name, percentage):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'GD_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
    #         check_query = f"SELECT COALESCE(SUM(percentage), 0) FROM {table_name}"
    #         cursor.execute(check_query)
    #         total_percentage = Decimal(cursor.fetchone()[0])
    #         percentage = Decimal(str(percentage))
    #         if total_percentage + percentage > 100:
    #             return "Sum of percentage values cannot exceed 100"
    #         insert_query = f"INSERT INTO {table_name} (name, percentage) VALUES (%s, %s)"
    #         values = (name, percentage)
    #         cursor.execute(insert_query, values)
    #         mysql.connection.commit()
    #         return "Assessment created successfully"
    #     except Exception as e:
    #         return f"{str(e)}"



    # @classmethod
    # def deleteGradeAssessment(cls, subject_code, section_code, school_year, sem, assessmentid):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'GD_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')

    #         cursor.execute(f"DELETE FROM {table_name} WHERE assessmentID = %s", (assessmentid,))
    #         mysql.connection.commit()

    #         cursor.execute(f"SET @new_assessmentID := 0;")
    #         cursor.execute(f"UPDATE {table_name} SET assessmentID = @new_assessmentID := @new_assessmentID + 1 ORDER BY assessmentid;")
    #         mysql.connection.commit()

    #         return "Assessment deleted successfully"
    #     except Exception as e:
    #         return f"Failed to delete assessment: {str(e)}"

    # @staticmethod
    # def getRowsClassRecord(subject_code, section_code, school_year, sem):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         table_name = f'CR_{subject_code}_{section_code}_{school_year}_{sem}'.replace('-', '_')
    #         sql = f"SELECT classID, studentID, firstname, lastname, email FROM {table_name}"
    #         cursor.execute(sql)
    #         result = cursor.fetchall()
    #         cursor.close()
    #         return result
    #     except Exception as e:
    #         return f"Failed to fetch students: {str(e)}"