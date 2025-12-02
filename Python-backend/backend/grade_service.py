from .database import get_connection


def create_grade(matno, pnr, grade, grade_date):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO grade (matno, pnr, grade, grade_date)
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
        SELECT grade.pnr, exam.title, grade.grade, grade.grade_date
        FROM grade
        JOIN exam ON grade.pnr = exam.pnr
        WHERE grade.matno = %s
        ORDER BY exam.title ASC
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
        FROM grade
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

    sql = f"UPDATE grade SET {', '.join(sql_parts)} WHERE matno = %s AND pnr = %s"
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
        sql = "DELETE FROM grade WHERE matno = %s AND pnr = %s"
        cur.execute(sql, (matno, pnr))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Fehler beim Löschen der Note:", e)
    finally:
        cur.close()
        conn.close()
