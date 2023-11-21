from app import mysql

class SubjectList(object):
    def __init__(self, code, section, description, credits, handler, semester) -> None:
        self.code = code
        self.section = section
        self.description = description
        self.credits = credits
        self.handler = handler
        self.semester = semester
    
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
