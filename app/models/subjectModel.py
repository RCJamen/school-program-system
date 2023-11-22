from app import mysql

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
            sql_assign_faculty = "INSERT INTO assignFaculty(facultyID, subjectID, sectionID) VALUES (%s, %s, %s)"
            params_subject = (self.code, self.description, self.credits)
            params_section = (self.code, self.section)
            params_assign_faculty = (self.handler, self.code, self.section)
            cursor.execute(sql_subject, params_subject)
            cursor.execute(sql_section, params_section)
            cursor.execute(sql_assign_faculty, params_assign_faculty)
            mysql.connection.commit()
            return "Faculty created successfully"
        except Exception as e:
            return f"Failed to create Faculty: {str(e)}"

    @classmethod
    def delete(cls, subjectCode, section):
        try:
            cursor = mysql.connection.cursor()
            subject_section = "DELETE FROM subject_section WHERE subjectID = %s AND sectionID = %s"
            assign_faculty = "DELETE FROM assignFaculty WHERE subjectID = %s AND sectionID = %s"         
            subject = "DELETE FROM subject WHERE subjectCode = %s"            
            params_subject_section = (subjectCode, section)
            params_assign_faculty = (subjectCode, section)
            params_subject = (subjectCode,)
            cursor.execute(subject_section, params_subject_section)
            cursor.execute(assign_faculty, params_assign_faculty)
            cursor.execute(subject, params_subject)
            mysql.connection.commit()
            return "Subject deleted successfully"
        except Exception as e:
            return f"Failed to delete Subject: {str(e)}"
        finally:
            cursor.close()


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
        sql = f"SELECT facultyID, firstname, lastname FROM faculty"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def all(cls):
        try:
            cursor = mysql.connection.cursor()
            sql = '''SELECT 
                        s.subjectCode,
                        ss.sectionID,
                        s.description,
                        s.credits,
                        CONCAT(f.firstname, ' ', f.lastname) AS handlerName
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
    def getSubjectsHandled(cls, handlerName):
        try:
            cursor = mysql.connection.cursor()
            sql = '''SELECT 
                        s.subjectCode, 
                        af.sectionID, 
                        s.description, 
                        s.credits 
                    FROM 
                        assignFaculty AS af
                    LEFT JOIN 
                        subject AS s ON af.subjectID = s.subjectCode
                    LEFT JOIN
                        faculty AS f ON af.facultyID = f.facultyID
                    WHERE 
                        CONCAT(f.firstname, ' ', f.lastname) = %s
                    ORDER BY s.subjectCode, af.sectionID'''
            cursor.execute(sql, (handlerName,))
            result = cursor.fetchall()
            return result
        except Exception as e:
            return f"Failed to load list of Subjects Handled: {str(e)}"

    
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
