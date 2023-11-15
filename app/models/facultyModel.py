from app import mysql

class facultyModel:
    @classmethod
    def create_faculty(cls, facultyID, firstname, lastname, email):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("INSERT INTO faculty (facultyID, firstname, lastname, email) VALUES (%s, %s, %s, %s)", (facultyID, firstname, lastname, email))
            mysql.connection.commit()
            return "Faculty created successfully"
        except Exception as e:
            return f"Failed to create Faculty: {str(e)}"

    @classmethod
    def get_faculty(cls):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("SELECT facultyID, firstname, lastname, email FROM faculty")
            faculties = cur.fetchall()
            return faculties
        except Exception as e:
            return f"Failed to retrieve faculty data: {str(e)}"
        
    # @classmethod
    # def get_single_faculty(cls, facultyID):
    #     try:
    #         cur = mysql.connection.cursor(dictionary=True)
    #         cur.execute("SELECT facultyID, firstname, lastname, email FROM faculty WHERE facultyID = %s", (facultyID,))
    #         faculty = cur.fetchone()
    #         return faculty
    #     except Exception as e:
    #         return f"Failed to retrieve faculty data: {str(e)}"
    #     finally:
    #         cur.close()

    @classmethod
    def delete_faculty(cls, facultyID):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute("DELETE FROM faculty where facultyID = %s", (facultyID,))
            mysql.connection.commit()
            return "Faculty deleted successfully"
        except Exception as e:
            return f"Failed to delete faculty: {str(e)}"
