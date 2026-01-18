from .database import get_connection

def create_exam(pnr, title, semester, degree):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO exams (pnr, title, semester, degree)
        VALUES (%s, %s, %s, %s)
    """
    cur.execute(sql, (pnr, title, semester, degree))
    conn.commit()
    cur.close()
    conn.close()

def get_all_exams():
    conn = get_connection()
    cur = conn.cursor()
    # Explizite Auswahl der verbleibenden Spalten
    cur.execute("SELECT pnr, title, semester, degree FROM exams ORDER BY pnr ASC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def update_exam(pnr, title=None, semester=None, degree=None):
    conn = get_connection()
    cur = conn.cursor()

    sql_parts = []
    values = []

    if title:
        sql_parts.append("title = %s")
        values.append(title)
    if semester is not None:
        sql_parts.append("semester = %s")
        values.append(semester)
    if degree:
        sql_parts.append("degree = %s")
        values.append(degree)

    if not sql_parts:
        print("Keine Daten zum Aktualisieren angegeben.")
        return

    sql = f"UPDATE exams SET {', '.join(sql_parts)} WHERE pnr = %s"
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

# In exam_service.py

def delete_exam(pnr):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "DELETE FROM exams WHERE pnr = %s"
        # Stellen Sie sicher, dass pnr den richtigen Typ hat
        # Wenn pnr in der DB ein INTEGER ist:
        pnr_int = int(pnr)
        cur.execute(sql, (pnr_int,))
        # Wenn pnr in der DB ein VARCHAR ist:
        # pnr_str = str(pnr)
        # cur.execute(sql, (pnr_str,))
        conn.commit()
    except ValueError:
        print(f"Ungültiger PNr-Wert: {pnr}")
        conn.rollback()
    except Exception as e:
        conn.rollback()
        print("Fehler beim Löschen der Prüfung:", e)
    finally:
        cur.close()
        conn.close()