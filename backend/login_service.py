from .database import get_connection

def verify_login(employee_id, password):
    """
    Überprüft die Login-Daten eines Mitarbeiters.
    
    Args:
        employee_id: Die Mitarbeiter-ID
        password: Das Passwort
    
    Returns:
        Tuple (role, name) wenn Login erfolgreich, sonst None
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            SELECT employee_role, employee_name 
            FROM roles 
            WHERE employee_id = %s AND employee_password = %s
        """
        cur.execute(sql, (int(employee_id), password))
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result:
            return result  # Gibt (role, name) zurück
        return None
    except Exception as e:
        print(f"Login-Fehler: {e}")
        return None

def get_employee_by_id(employee_id):
    """
    Holt Mitarbeiterdaten anhand der ID.
    
    Args:
        employee_id: Die Mitarbeiter-ID
    
    Returns:
        Dict mit Mitarbeiterdaten oder None
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            SELECT employee_id, employee_name, employee_role
            FROM roles 
            WHERE employee_id = %s
        """
        cur.execute(sql, (int(employee_id),))
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'role': result[2]
            }
        return None
    except Exception as e:
        print(f"Fehler beim Abrufen des Mitarbeiters: {e}")
        return None

def get_all_employees():
    """
    Holt alle Mitarbeiter aus der Datenbank.
    
    Returns:
        Liste von Tuples (id, name, role)
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = """
            SELECT employee_id, employee_name, employee_role
            FROM roles 
            ORDER BY employee_id ASC
        """
        cur.execute(sql)
        results = cur.fetchall()
        cur.close()
        conn.close()
        
        return results
    except Exception as e:
        print(f"Fehler beim Abrufen aller Mitarbeiter: {e}")
        return []