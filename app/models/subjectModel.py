from app import mysql
import csv
class Subjects(object):
    def __init__(self, code, section, description, credits, handler) -> None:
        self.code = code
        self.section = section
        self.description = description
        self.credits = credits
        self.handler = handler
    
    def add(self):
        try:
            cursor = mysql.connection.cursor()
            sql_subject = "INSERT INTO subject(subjectCode, description, credits) VALUES (%s, %s, %s)"
            sql_section = "INSERT INTO subject_section(subjectID, sectionID) VALUES (%s, %s)"
            sql_assignFaculty = "INSERT INTO assignFaculty(facultyID, subjectID, sectionID) VALUES (%s, %s, %s)"
            params_subject = (self.code, self.description, self.credits)
            params_section = (self.code, self.section)
            params_assignFaculty = (self.handler, self.code, self.section)
            cursor.execute(sql_subject, params_subject)
            cursor.execute(sql_section, params_section)
            cursor.execute(sql_assignFaculty, params_assignFaculty)
            mysql.connection.commit()
            return "Faculty created successfully"
        except Exception as e:
            return f"Failed to create Faculty: {str(e)}"    
        
    def add_section(self):
        try:
            cursor = mysql.connection.cursor()
            sql_section = "INSERT INTO subject_section(subjectID, sectionID) VALUES (%s, %s)"
            sql_assignFaculty = "INSERT INTO assignFaculty(facultyID, subjectID, sectionID) VALUES (%s, %s, %s)"
            params_section = (self.code, self.section)
            params_assignFaculty = (self.handler, self.code, self.section)
            cursor.execute(sql_section, params_section)
            cursor.execute(sql_assignFaculty, params_assignFaculty)
            mysql.connection.commit()
            return "Faculty created successfully"
        except Exception as e:
            return f"Failed to create Faculty: {str(e)}"    

    
    csv_data = None

    @classmethod
    def load_csv_data(cls, file):
        file_content = file.read().decode('utf-8').splitlines()
        cls.csv_data = list(csv.reader(file_content))

    @classmethod
    def upload_subject(cls, file):
        cursor = None  # Initialize cursor outside the try block
        try:
            # Check if the file is provided and has a CSV extension
            if file and file.filename.endswith('.csv'):
                # Load CSV data
                if cls.csv_data is None:  # Check if CSV data is not yet loaded
                    cls.load_csv_data(file)  # Load CSV data
                    
                # Continue with the rest of the code
                cursor = mysql.connection.cursor()

                # Iterate over CSV data, starting from the second row to skip the header
                for row in cls.csv_data[1:]:
                    code = row[0]
                    description = row[2]  # Assuming Description is in the third column
                    credits = row[3]  # Assuming Credits is in the fourth column
                    section = row[1]  # Assuming Section is in the second column
                    handler = row[4]
                    sem = row[5]
                    schoolyear = row[6]

                    # Print the entire row for debugging
                    print(f"Current Row: {row}")

                    # Print individual fields for debugging
                    print(f"Code: {code}, Section: {section}, Description: {description}, Credits: {credits}, Handler: {handler}")
                    sql_subject = "INSERT INTO subject(subjectCode, description, credits) VALUES (%s, %s, %s)"
                    sql_section = "INSERT INTO subject_section(subjectID, sectionID) VALUES (%s, %s)"
                    sql_assignFaculty = "INSERT INTO assignFaculty(facultyID, subjectID, sectionID, sem, schoolYear) VALUES (%s, %s, %s, %s, %s)"
                    params_subject = (code, description, credits)
                    params_section = (code, section)
                    params_assignFaculty = (handler, code, section, sem, schoolyear)

                    cursor.execute(sql_subject, params_subject)
                    cursor.execute(sql_section, params_section)
                    cursor.execute(sql_assignFaculty, params_assignFaculty)

                # Commit the changes to the database
                mysql.connection.commit()

                return {"type": "success", "message": 'File uploaded and data inserted successfully.'}

            else:
                return {"type": "danger", "message": 'Invalid file format. Please upload a CSV file.'}

        except Exception as e:
            error_message = f'Error: {str(e)}'
            return {"type": "danger", "message": error_message}

        finally:
            if cursor:
                cursor.close()  # Close the cursor to release resources

    @classmethod
    def truncate_subject(cls):
        try:
            cursor = mysql.connection.cursor()

            # Disable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            # Truncate tables
            cursor.execute("TRUNCATE TABLE subject")
            cursor.execute("TRUNCATE TABLE subject_section")
            cursor.execute("TRUNCATE TABLE assignFaculty")

            # Enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            mysql.connection.commit()

            return "Subject truncated successfully"
        
        except mysql.connector.Error as err:
            return f"MySQL Error: {err}"
        
        except Exception as e:
            return f"Error: {str(e)}"


    
    @classmethod
    def delete(cls, subjectCode, section, handler):
        try:
            cursor = mysql.connection.cursor()

            sql_get_faculty_id = "SELECT facultyID FROM faculty WHERE CONCAT(firstname, ' ', lastname) LIKE %s"
            cursor.execute(sql_get_faculty_id, (f"%{handler}%",))
            faculty_id_result = cursor.fetchone()
            facultyID = faculty_id_result[0]

            sql_get_assignFaculty = "SELECT assignFacultyID FROM assignFaculty WHERE facultyID = %s AND subjectID = %s AND sectionID = %s"
            cursor.execute(sql_get_assignFaculty, (facultyID, subjectCode, section))
            assignFacultyID_result = cursor.fetchone()
            assignFacultyID = assignFacultyID_result[0]

            sql_get_subject_section = "SELECT subsecID FROM subject_section WHERE subjectID = %s AND sectionID = %s"
            cursor.execute(sql_get_subject_section, (subjectCode, section))
            subsecID_result = cursor.fetchone()
            subsecID = subsecID_result[0]
            
            subject_section = "DELETE FROM subject_section WHERE subsecID = %s"
            assignFaculty = "DELETE FROM assignFaculty WHERE assignFacultyID = %s"         
            subject = "DELETE FROM subject WHERE subjectCode = %s"    

            params_subject_section = (subsecID,)
            params_assignFaculty = (assignFacultyID,)
            params_subject = (subjectCode,)

            cursor.execute(subject_section, params_subject_section)
            cursor.execute(assignFaculty, params_assignFaculty)
            cursor.execute(subject, params_subject)
            mysql.connection.commit()
            return "Subject deleted successfully"
        except Exception as e:
            print(e)
            return f"Failed to delete Subject: {str(e)}"
        finally:
            cursor.close()

    @classmethod
    def delete_section(cls, subjectCode, section, handler):
        try:
            cursor = mysql.connection.cursor()

            sql_get_faculty_id = "SELECT facultyID FROM faculty WHERE CONCAT(firstname, ' ', lastname) LIKE %s"
            cursor.execute(sql_get_faculty_id, (f"%{handler}%",))
            faculty_id_result = cursor.fetchone()
            facultyID = faculty_id_result[0]

            sql_get_assignFaculty = "SELECT assignFacultyID FROM assignFaculty WHERE facultyID = %s AND subjectID = %s AND sectionID = %s"
            cursor.execute(sql_get_assignFaculty, (facultyID, subjectCode, section))
            assignFacultyID_result = cursor.fetchone()
            assignFacultyID = assignFacultyID_result[0]

            sql_get_subject_section = "SELECT subsecID FROM subject_section WHERE subjectID = %s AND sectionID = %s"
            cursor.execute(sql_get_subject_section, (subjectCode, section))
            subsecID_result = cursor.fetchone()
            subsecID = subsecID_result[0]
            
            subject_section = "DELETE FROM subject_section WHERE subsecID = %s"
            assignFaculty = "DELETE FROM assignFaculty WHERE assignFacultyID = %s"         

            params_subject_section = (subsecID,)
            params_assignFaculty = (assignFacultyID,)

            cursor.execute(subject_section, params_subject_section)
            cursor.execute(assignFaculty, params_assignFaculty)
            mysql.connection.commit()
            return "Subject deleted successfully"
        except Exception as e:
            return f"Failed to delete Subject: {str(e)}"
        finally:
            cursor.close()


    @staticmethod
    def update(subjectCode, old_subjectCode, section, old_sectionCode, description, credits, handler, old_handlerCode):
        try:
            cursor = mysql.connection.cursor()

            sql_get_faculty_id = "SELECT facultyID FROM faculty WHERE CONCAT(firstname, ' ', lastname) LIKE %s"
            cursor.execute(sql_get_faculty_id, (f"%{old_handlerCode}%",))
            faculty_id_result = cursor.fetchone()
            old_facultyID = faculty_id_result[0]

            sql_get_assignFaculty = "SELECT assignFacultyID FROM assignFaculty WHERE facultyID = %s AND subjectID = %s AND sectionID = %s"
            cursor.execute(sql_get_assignFaculty, (old_facultyID, old_subjectCode, old_sectionCode))
            assignFacultyID_result = cursor.fetchone()
            old_assignFacultyID = assignFacultyID_result[0]

            sql_get_subject_section = "SELECT subsecID FROM subject_section WHERE subjectID = %s AND sectionID = %s"
            cursor.execute(sql_get_subject_section, (old_subjectCode, old_sectionCode))
            subsecID_result = cursor.fetchone()
            old_subsecID = subsecID_result[0]

            sql_subject_update = "UPDATE subject SET subjectCode= %s, description = %s, credits = %s WHERE subjectCode = %s"
            params_subject_update = (subjectCode, description, credits, old_subjectCode)
            cursor.execute(sql_subject_update, params_subject_update)

            sql_assign_faculty_update = "UPDATE assignFaculty SET facultyID = %s, subjectID = %s, sectionID = %s WHERE assignFacultyID = %s"
            params_assign_faculty_update = (handler, subjectCode, section, old_assignFacultyID)
            cursor.execute(sql_assign_faculty_update, params_assign_faculty_update)

            sql_section_update = "UPDATE subject_section SET subjectID = %s, sectionID = %s WHERE subsecID = %s"
            params_section_update = (subjectCode, section, old_subsecID)
            cursor.execute(sql_section_update, params_section_update)

            mysql.connection.commit()
            return "Subject edited successfully"
        except Exception as e:
            return f"Failed to edit subject: {str(e)}"
        

    @classmethod
    def exists(cls, code):
        cursor = mysql.connection.cursor()
        check_sql = "SELECT subjectCode FROM subject WHERE subjectCode = %s"
        cursor.execute(check_sql, (code,))
        existing_subject = cursor.fetchone()
        return existing_subject is not None

    @classmethod
    def exists_many(cls, code):
        cursor = mysql.connection.cursor()
        check_sql = "SELECT COUNT(*) FROM subject_section WHERE subjectID = %s"
        cursor.execute(check_sql, (code,))
        result = cursor.fetchone()
        count = result[0]
        cursor.close()
        print(f"Count of existing subjects: {count}")
        return count > 0

    @classmethod
    def refer_section(cls):
        cursor = mysql.connection.cursor()
        sql = f"SELECT sectionCode FROM section"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    
    @classmethod
    def refer_handler(cls):
        cursor = mysql.connection.cursor()
        sql = f"SELECT facultyID, firstname, lastname FROM faculty WHERE facultyID != 'None'"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def get_id(self, old_handlerCode):
        cursor = mysql.connection.cursor()
        sql = "SELECT facultyID FROM faculty WHERE CONCAT(firstname, ' ', lastname) LIKE %s"
        params_sql= (old_handlerCode,)
        cursor.execute(sql, params_sql)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None 

    @classmethod
    def all(cls):
        try:
            cursor = mysql.connection.cursor()
            sql = '''SELECT 
                        s.subjectCode,
                        ss.sectionID,
                        s.description,
                        s.credits,
                        CASE WHEN f.firstname = f.lastname THEN f.firstname
                            ELSE CONCAT(f.firstname, ' ', f.lastname) END AS handlerName
                    FROM 
                        subject AS s
                    LEFT JOIN 
                        subject_section AS ss ON s.subjectCode = ss.subjectID
                    LEFT JOIN 
                        assignFaculty AS af ON ss.subjectID = af.subjectID AND ss.sectionID = af.sectionID
                    LEFT JOIN 
                        faculty AS f ON af.facultyID = f.facultyID
                    ORDER BY s.subjectCode, ss.sectionID'''
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            return f"Failed to load Subject List: {str(e)}"
    
    @classmethod    
    def getSubjectsHandled(cls, userEmail):
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
                        f.email = %s
                    ORDER BY s.subjectCode, af.sectionID'''
                        # f.facultyID = (SELECT facultyID from faculty where email = %s)
            cursor.execute(sql, (userEmail,))
            result = cursor.fetchall()
            return result
        except Exception as e:
            return f"Failed to load list of Subjects Handled: {str(e)}"

    # supposedly, to map google_id to user's facultyID
    # @classmethod
    # def setGoogleID(cls, googleID, userEmail):
    #     try:
    #         cursor = mysql.connection.cursor()
    #         sql = '''UPDATE faculty
    #                 SET
    #                     googleID = %s
    #                 WHERE
    #                     email = %s'''
    #         cursor.execute(sql, (googleID, userEmail,))
    #         mysql.connection.commit()
    #     except Exception as e:
    #         return f"Failed to set Google ID: {str(e)}"

    
    # GET LIST OF SUBJECTS BY SEMESTER
    # def semester(cls, sem):
    #     cursor = mysql.connection.cursor()
    #     sql = '''SELECT sl.subjectCode, s.sectionCode, sl.description, sl.credits, concat(f.firstname, ' ', f.lastname) AS handlerName FROM sections AS s 
    #             RIGHT JOIN faculty AS f ON s.handlerID = f.facultyID 
    #             RIGHT JOIN subjectList AS sl ON s.subjectCode = sl.subjectCode
    #             WHERE sl.semester = 1'''
    #     cursor.execute(sql)
    #     result = cursor.fetchall()

    #     return result
