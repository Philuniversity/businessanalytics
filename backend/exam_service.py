from .database import get_connection


def create_exam(pnr, title, exam_date, semester, degree):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO exam (pnr, title, exam_date, semester, degree)
        VALUES (%s, %s, %s, %s, %s)
    """
    cur.execute(sql, (pnr, title, exam_date, semester, degree))
    conn.commit()
    cur.close()
    conn.close()


def get_all_exams():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM exam ORDER BY pnr ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def update_exam(pnr, title=None, exam_date=None, semester=None, degree=None):
    conn = get_connection()
    cur = conn.cursor()

    sql_parts = []
    values = []

    if title:
        sql_parts.append("title = %s")
        values.append(title)
    if exam_date:
        sql_parts.append("exam_date = %s")
        values.append(exam_date)
    if semester is not None:
        sql_parts.append("semester = %s")
        values.append(semester)
    if degree:
        sql_parts.append("degree = %s")
        values.append(degree)

    if not sql_parts:
        print("Keine Daten zum Aktualisieren angegeben.")
        return

    sql = f"UPDATE exam SET {', '.join(sql_parts)} WHERE pnr = %s"
    values.append(pnr)

    try:
        cur.execute(sql, tuple(values))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Fehler bei update_exam:", e)
    finally:
        cur.close()
        conn.close()


def delete_exam(pnr):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "DELETE FROM exam WHERE pnr = %s"
        cur.execute(sql, (pnr,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Fehler beim Löschen der Prüfung:", e)
    finally:
        cur.close()
        conn.close()
