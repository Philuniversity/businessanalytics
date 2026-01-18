from .database import get_connection


def create_grade(matno, pnr, grade, grade_date):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO grades (matno, pnr, grade, grade_date)
        VALUES (%s, %s, %s, %s)
    """
    cur.execute(sql, (matno, pnr, grade, grade_date))
    conn.commit()
    cur.close()
    conn.close()


def get_grades_for_student(matno):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        SELECT grades.pnr, exams.title, grades.grade, 
               TO_CHAR(grades.grade_date, 'DD-MM-YYYY') as grade_date
        FROM grades
        JOIN exams ON grades.pnr = exams.pnr
        WHERE grades.matno = %s
        ORDER BY exams.title ASC
    """
    cur.execute(sql, (matno,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_exam_statistics(pnr):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        SELECT 
            AVG(grade) AS average_grade,
            MIN(grade) AS min_grade,
            MAX(grade) AS max_grade,
            COUNT(*) AS participant_count
        FROM grades
        WHERE pnr = %s
    """
    cur.execute(sql, (pnr,))
    stats = cur.fetchone()
    cur.close()
    conn.close()
    return stats


def update_grade(matno, pnr, grade=None, grade_date=None):
    conn = get_connection()
    cur = conn.cursor()

    sql_parts = []
    values = []

    if grade is not None:
        sql_parts.append("grade = %s")
        values.append(grade)
    if grade_date:
        sql_parts.append("grade_date = %s")
        values.append(grade_date)

    if not sql_parts:
        print("Keine Änderungen angegeben.")
        return

    sql = f"UPDATE grades SET {', '.join(sql_parts)} WHERE matno = %s AND pnr = %s"
    values.extend([matno, pnr])

    try:
        cur.execute(sql, tuple(values))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Fehler bei update_grade:", e)
    finally:
        cur.close()
        conn.close()


def delete_grade(matno, pnr):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "DELETE FROM grades WHERE matno = %s AND pnr = %s"
        cur.execute(sql, (matno, pnr))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Fehler beim Löschen der Note:", e)
    finally:
        cur.close()
        conn.close()
