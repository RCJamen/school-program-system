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
            sql = '''SELECT sub.subjectCode, s.sectionCode, sub.description, sub.credits, concat(f.firstname, ' ', f.lastname) AS handlerName FROM assignFaculty AS af
                    RIGHT JOIN subject AS sub ON af.subjectID = sub.subjectCode
                    LEFT JOIN faculty AS f ON f.facultyID = af.facultyID
                    LEFT JOIN section AS s ON af.sectionID = s.sectionCode
                    ORDER BY sub.subjectCode, s.sectionCode'''
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            return f"Failed to load Subject List: {str(e)}"

    
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
