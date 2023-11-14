from app import mysql

class SubjectList(object):
    def __init__(self, code, section, description, credits, handler) -> None:
        self.code = code
        self.section = section
        self.description = description
        self.credits = credits
        self.handler = handler
    
    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM sections RIGHT JOIN subjectList ON sections.subjectCode = subjectList.subjectCode ORDER BY sectionCode"
        cursor.execute(sql)
        result = cursor.fetchall()

        return result