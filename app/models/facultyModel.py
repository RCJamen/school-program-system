from app import mysql
from datetime import timedelta

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
            cur.execute("SELECT facultyID, firstname, lastname, email FROM faculty WHERE facultyID != 'None'")
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
    
    
    def get_assigned_subjects(self, faculty_id):
        try:
            cur = mysql.new_cursor(dictionary=True)
            query = (
                "SELECT "
                "   af.subjectID AS 'Subject Code', "
                "   subject.description AS 'Description', "
                "   subject.credits AS 'Credits', "
                "   af.sectionID AS 'Section ID', "
                "   CASE "
                "       WHEN CONCAT(IFNULL(s.day, 'None'), ' ', "
                "                   IFNULL(TIME_FORMAT(s.time_start, '%h:%i %p'), 'None'), ' - ', "
                "                   IFNULL(TIME_FORMAT(s.time_end, '%h:%i %p'), 'None')) = 'None None - None' "
                "       THEN 'None' "
                "       ELSE CONCAT(IFNULL(s.day, 'None'), ' ', "
                "                   IFNULL(TIME_FORMAT(s.time_start, '%h:%i %p'), 'None'), ' - ', "
                "                   IFNULL(TIME_FORMAT(s.time_end, '%h:%i %p'), 'None')) "
                "   END AS 'Schedule' "
                "FROM assignFaculty af "
                "JOIN subject ON subject.subjectCode = af.subjectID "
                "LEFT JOIN schedule s ON af.subjectID = s.subjectID AND af.sectionID = s.sectionID "
                "WHERE af.facultyID = %s"
            )
            cur.execute(query, (faculty_id,))
            assigned_subjects = cur.fetchall()
            cur.close()
            return assigned_subjects
        except Exception as e:
            return f"Failed to retrieve assigned subject to faculty data: {str(e)}"

    @classmethod
    def create_schedule(cls, subjectID, sectionID, day, time_start, time_end):
        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(
                "INSERT INTO schedule (subjectID, sectionID, day, time_start, time_end) VALUES (%s, %s, %s, %s, %s)",
                (subjectID, sectionID, day, time_start, time_end),
            )
            mysql.connection.commit()
            return "Schedule created successfully"
        except Exception as e:
            return f"Failed to create schedule: {str(e)}"

    # def check_schedule_conflict(self, subjectID, sectionID, day, time_start, time_end, current_schedule_id=None):
    #     cur = mysql.connection.cursor(dictionary=True)

    #     # Prepare the query
    #     query = (
    #         "SELECT * FROM schedule "
    #         "WHERE subjectID = %s AND sectionID = %s AND day = %s "
    #         "AND NOT (time_end <= %s OR time_start >= %s)"
    #     )

    #     # If current_schedule_id is provided, exclude it from the conflict check
    #     if current_schedule_id:
    #         query += " AND scheduleID != %s"

    #     cur.execute(query, (subjectID, sectionID, day, time_start, time_end, current_schedule_id))
    #     conflicting_schedules = cur.fetchall()
    #     cur.close()

    #     return conflicting_schedules

    @classmethod
    def get_schedule_monday(self, faculty_id):
        try:
            cur = mysql.new_cursor(dictionary=True)

            # Print the SQL query and parameters for debugging
            query = f"""
                SELECT
                    schedule.scheduleID,
                    schedule.subjectID,
                    schedule.sectionID,
                    schedule.day,
                    TIME_FORMAT(schedule.time_start, '%H:%i:%s') as time_start,
                    TIME_FORMAT(schedule.time_end, '%H:%i:%s') as time_end
                FROM
                    schedule
                JOIN
                    assignFaculty ON schedule.subjectID = assignFaculty.subjectID AND schedule.sectionID = assignFaculty.sectionID
                JOIN
                    faculty ON assignFaculty.facultyID = faculty.facultyID
                WHERE
                    schedule.day = 'Monday'
                    AND faculty.facultyID = '{faculty_id}';
            """

            print("SQL Query:", query)

            cur.execute(query)
            schedules = cur.fetchall()
            cur.close()
            return schedules
        except Exception as e:
            return f"Failed to retrieve Monday schedule data: {str(e)}"


