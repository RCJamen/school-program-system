from app import mysql


class facultyModel:
    @classmethod
    def create_faculty(cls, facultyID, firstname, lastname, email):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(
                "INSERT INTO faculty (facultyID, firstname, lastname, email) VALUES (%s, %s, %s, %s)",
                (facultyID, firstname, lastname, email),
            )
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

    @classmethod
    def update_faculty(cls, facultyID, firstname, lastname, email):
        try:
            cur = mysql.new_cursor(dictionary=True)
            # Use placeholders in the query to prevent SQL injection
            cur.execute("UPDATE faculty SET firstname = %s, lastname = %s, email = %s WHERE facultyID = %s",
                        (firstname, lastname, email, facultyID))
            mysql.connection.commit()
            return "Faculty Information Updated Successfully"
        except Exception as e:
            return f"Failed to update faculty: {str(e)}"
    
    
    @classmethod
    def update_faculty(cls, facultyID):
        try:
            cur = mysql.new_cursor(dictionary=True)
            query = """
            SELECT subject.subjectCode, subject.description, subject.credits, subject.semester
            FROM assignFaculty
            JOIN subject ON assignFaculty.subjectID = subject.subjectCode
            WHERE assignFaculty.facultyID = %s
        """
            # Use placeholders in the query to prevent SQL injection
            cur.execute(query,
                        (facultyID))
            assigned_subjects = cur.fetchall()
            mysql.connection.commit()
            return assigned_subjects
        except Exception as e:
            return f"Failed to update faculty: {str(e)}"
    
    def get_assigned_subjects(self, faculty_id):
        try:
            cur = mysql.new_cursor(dictionary=True)
            query = (
                "SELECT "
                "   af.subjectID AS 'Subject Code', "
                "   subject.description AS 'Description', "
                "   subject.credits AS 'Credits', "
                "   af.sectionID AS 'Section ID' "
                "FROM assignFaculty af "
                "JOIN subject ON subject.subjectCode = af.subjectID "
                "WHERE af.facultyID = %s"
            )
            cur.execute(query, (faculty_id,))
            assigned_subjects = cur.fetchall()
            cur.close()
            return assigned_subjects
        except Exception as e:
            return f"Failed to retrieve assigned subject to faculty data: {str(e)}"

