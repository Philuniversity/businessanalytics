from .database import get_connection


def create_student(matno, firstname, lastname, date_of_birth, semester, degree):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO student (matno, firstname, lastname, date_of_birth, semester, degree)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(sql, (matno, firstname, lastname, date_of_birth, semester, degree))
    conn.commit()
    cur.close()
    conn.close()


def get_all_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM student ORDER BY matno ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def update_student(matno, firstname=None, lastname=None, date_of_birth=None, semester=None, degree=None):
    conn = get_connection()
    cur = conn.cursor()

    sql_parts = []
    values = []

    if firstname:
        sql_parts.append("firstname = %s")
        values.append(firstname)
    if lastname:
        sql_parts.append("lastname = %s")
        values.append(lastname)
    if date_of_birth:
        sql_parts.append("date_of_birth = %s")
        values.append(date_of_birth)
    if semester is not None:
        sql_parts.append("semester = %s")
        values.append(semester)
    if degree:
        sql_parts.append("degree = %s")
        values.append(degree)

    if not sql_parts:
        print("Keine Daten zum Aktualisieren angegeben.")
        return

    sql = f"UPDATE student SET {', '.join(sql_parts)} WHERE matno = %s"
    values.append(matno)

    try:
        cur.execute(sql, tuple(values))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Fehler bei update_student:", e)
    finally:
        cur.close()
        conn.close()


def delete_student(matno):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "DELETE FROM student WHERE matno = %s"
        cur.execute(sql, (matno,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Fehler beim Löschen des Studenten:", e)
    finally:
        cur.close()
        conn.close()
