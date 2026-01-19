import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from backend.login_service import verify_login
from backend.exam_service import create_exam, get_all_exams, update_exam, delete_exam
from backend.student_service import create_student, get_all_students, update_student, delete_student
from backend.grade_service import create_grade, get_grades_for_student, get_exam_statistics, update_grade, delete_grade


#############################
#### Login Fenster class ####
#############################
# Erstellen des LoginWindows, welche bei der Exammanagement app selbst gecalled wird.
# Diese Klasse ist nur das styling und die Funktionsabfrage der login_service function (verify_login)
class LoginWindow:
    def __init__(self, root, on_login_success): #self, da object-oriented, root ist das Hauptfenster
        self.root = root
        self.on_login_success = on_login_success
        
        self.login_window = tk.Toplevel(root)
        self.login_window.title("Login - Prüfungsverwaltungssystem")
        self.login_window.geometry("400x250")
        self.login_window.resizable(False, False)
        self.login_window.grab_set()
        
        # Center window and make modal
        self.login_window.transient(root)
        self.login_window.protocol("WM_DELETE_WINDOW", self.on_close)
        

        #Anmelde-fenster
        login_frame = ttk.Frame(self.login_window, padding=20)
        login_frame.pack(fill='both', expand=True)
        
        ttk.Label(login_frame, text="Anmeldung", font=('Arial', 14, 'bold')).pack(pady=(0, 20))

        id_frame = ttk.Frame(login_frame)
        id_frame.pack(fill='x', pady=5)
        ttk.Label(id_frame, text="Mitarbeiter ID:", width=15).pack(side='left')
        self.employee_id_entry = ttk.Entry(id_frame)
        self.employee_id_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))

        password_frame = ttk.Frame(login_frame)
        password_frame.pack(fill='x', pady=5)
        ttk.Label(password_frame, text="Passwort:", width=15).pack(side='left')
        self.password_entry = ttk.Entry(password_frame, show="*")
        self.password_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))

        # Login Button/ Enter-Taste
        ttk.Button(login_frame, text="Login", command=self.verify_login).pack(pady=20)
        self.employee_id_entry.bind('<Return>', lambda e: self.verify_login()) # Enter-Taste für Login, wenn man bei ID schreibt
        self.password_entry.bind('<Return>', lambda e: self.verify_login()) # Enter-Taste für Login, wenn man bei password schreibt
        
        self.employee_id_entry.focus_set()
    
    def on_close(self):
        self.root.quit() # Beendet die gesamte Anwendung, wenn das Login-Fenster geschlossen wird
    
    def verify_login(self):
        employee_id = self.employee_id_entry.get()
        password = self.password_entry.get()
        
        if not employee_id or not password:
            messagebox.showwarning("Warnung", "Bitte geben Sie ID und Passwort ein!")
            return
        
        try:
            result = verify_login(employee_id, password) # Call login_service.py function
            
            if result:
                role, name = result
                self.login_window.destroy() # Schließe das Login-Fenster
                self.on_login_success(role, employee_id, name) # öffne Hauptfenster mit Benutzerinfo
            else:
                messagebox.showerror("Fehler", "Ungültige ID oder Passwort!")
                
        except Exception as e:
            messagebox.showerror("Fehler", f"Login-Fehler: {e}")


#######################
#### Hauptanwendung ###
#######################
# ExamManagementApp Klasse
##  
## create_exam_tab_content(self) -> verantwortlich für den Tab "Prüfungen"
#ä
class ExamManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prüfungsverwaltungssystem")
        self.root.geometry("1100x700")
        
        # User info
        self.current_user_role = None
        self.current_user_id = None
        self.current_user_name = None
        
        # Initialize tabs as None
        self.exam_tab = None
        self.student_tab = None
        self.grade_tab = None
        self.statistics_tab = None
        
        # Tab widgets that need to be initialized after login
        self.exam_tree = None #exam
        self.student_tree = None #student
        self.grade_tree = None # grade
        self.grade_student_combo = None # aktuell ungenutzt
        self.grade_exam_combo = None # aktuell ungenutzt
        self.grade_view_student_combo = None # aktuell ungenutzt
        self.stats_exam_combo = None # aktuell ungenutzt
        
        # Show login first
        self.show_login_window()
    
    def show_login_window(self):
        """Show login window"""
        LoginWindow(self.root, self.on_login_success)
    
    def on_login_success(self, role, user_id, user_name):
        """Called after successful login"""
        self.current_user_role = role
        self.current_user_id = user_id
        self.current_user_name = user_name
        
        # Initialize UI
        self.initialize_ui()
        
        # Load initial data based on role
        self.load_initial_data()
    
    def initialize_ui(self):
        """Initialize the main UI components"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # User info bar at top
        user_info_frame = ttk.Frame(self.root)
        user_info_frame.pack(side='top', fill='x', padx=10, pady=5)
        
        ttk.Label(user_info_frame, 
                 text=f"Eingeloggt als: {self.current_user_name} ({self.current_user_role} - ID: {self.current_user_id})",
                 font=('Arial', 10)).pack(side='left')
        
        ttk.Button(user_info_frame, text="Logout", command=self.logout).pack(side='right')
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create empty tabs first
        self.create_tab_containers()
        
        # Bind tab change event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        
        # Enable/disable tabs based on role
        self.setup_tab_access()
    
    def create_tab_containers(self):
        """Create empty tab containers"""
        self.exam_tab = ttk.Frame(self.notebook)
        self.student_tab = ttk.Frame(self.notebook)
        self.grade_tab = ttk.Frame(self.notebook)
        self.statistics_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.exam_tab, text="Prüfungen")
        self.notebook.add(self.student_tab, text="Studenten")
        self.notebook.add(self.grade_tab, text="Noten")
        self.notebook.add(self.statistics_tab, text="Statistiken")
    
    def setup_tab_access(self):
        """Enable/disable tabs based on role and populate accessible ones"""
        role_permissions = {
            'Professor': ['Noten', 'Statistiken'],
            'admin_exam': ['Prüfungen', 'Statistiken'],
            'admin_students': ['Studenten']
        }
        
        # Disable all tabs first
        for i in range(self.notebook.index('end')):
            tab_text = self.notebook.tab(i, 'text')
            self.notebook.tab(i, state='disabled')
        
        # Enable tabs based on role
        if self.current_user_role in role_permissions:
            allowed_tabs = role_permissions[self.current_user_role]
            for i in range(self.notebook.index('end')):
                tab_text = self.notebook.tab(i, 'text')
                if tab_text in allowed_tabs:
                    self.notebook.tab(i, state='normal')
        
        # Select first enabled tab
        for i in range(self.notebook.index('end')):
            if self.notebook.tab(i, 'state') == 'normal':
                self.notebook.select(i)
                break
    
    def load_initial_data(self):
        """Load initial data for the currently selected tab"""
        current_tab = self.notebook.tab(self.notebook.select(), 'text')
        self.load_tab_data(current_tab)
    
    def load_tab_data(self, tab_name):
        """Load data for specific tab"""
        if tab_name == "Prüfungen" and self.current_user_role == 'admin_exam':
            self.create_exam_tab_content()
            self.load_exams()
        
        elif tab_name == "Studenten" and self.current_user_role == 'admin_students':
            self.create_student_tab_content()
            self.load_students()
        
        elif tab_name == "Noten" and self.current_user_role == 'Professor':
            self.create_grade_tab_content()
            self.load_student_combo()
            self.load_exam_combo()
            self.load_students_for_grade_view()
            # Load grades for first student
            if self.grade_view_student_combo['values']:
                self.load_grades_for_selected_student()
        
        elif tab_name == "Statistiken":
            if self.current_user_role in ['Professor', 'admin_exam']:
                self.create_statistics_tab_content()
                self.load_stats_exam_combo()
                # Load stats for first exam
                if self.stats_exam_combo['values']:
                    self.load_exam_statistics()
    
    def on_tab_changed(self, event):
        """Handle tab change - check permissions and load data"""
        if not self.current_user_role:
            return
        
        current_tab_index = self.notebook.index('current')
        tab_name = self.notebook.tab(current_tab_index, 'text')
        
        # Check permissions
        tab_permissions = {
            'Prüfungen': ['admin_exam'],
            'Studenten': ['admin_students'],
            'Noten': ['Professor'],
            'Statistiken': ['Professor', 'admin_exam']
        }
        
        if tab_name in tab_permissions:
            if self.current_user_role not in tab_permissions[tab_name]:
                messagebox.showwarning("Zugriff verweigert", 
                                     f"Sie haben keine Berechtigung für den Tab '{tab_name}'!")
                
                # Switch to first accessible tab
                for i in range(self.notebook.index('end')):
                    tab_text = self.notebook.tab(i, 'text')
                    if (tab_text in tab_permissions and 
                        self.current_user_role in tab_permissions[tab_text]):
                        self.notebook.select(i)
                        return
            
            # Load data for this tab if not already loaded
            self.load_tab_data(tab_name)
    
    def logout(self):
        """Logout user"""
        if messagebox.askyesno("Logout", "Möchten Sie sich wirklich ausloggen?"):
            # Reset user info
            self.current_user_role = None
            self.current_user_id = None
            self.current_user_name = None
            
            # Clear all widgets
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Show login window again
            self.show_login_window()
    
    # ===== TAB CONTENT CREATION METHODS =====
    
    def create_exam_tab_content(self):
        """Create content for exams tab (only called when needed)"""
        if hasattr(self, 'exam_content_created') and self.exam_content_created:
            return
        
        # Clear existing widgets in exam tab
        for widget in self.exam_tab.winfo_children():
            widget.destroy()
        
        # Hauptcontainer mit 2 Spalten
        main_container = ttk.Frame(self.exam_tab)
        main_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Linke Spalte
        left_column = ttk.Frame(main_container)
        left_column.pack(side='left', fill='both', expand=True)
        
        # Eingabefelder
        input_frame = ttk.LabelFrame(left_column, text="Neue Prüfung anlegen", padding=10)
        input_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Prüfungsnummer (PNr):").grid(row=0, column=0, sticky='w', pady=5)
        self.exam_pnr_entry = ttk.Entry(input_frame, width=30)
        self.exam_pnr_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(input_frame, text="Titel:").grid(row=1, column=0, sticky='w', pady=5)
        self.exam_title_entry = ttk.Entry(input_frame, width=30)
        self.exam_title_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(input_frame, text="Semester:").grid(row=2, column=0, sticky='w', pady=5)
        self.exam_semester_entry = ttk.Entry(input_frame, width=30)
        self.exam_semester_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(input_frame, text="Studiengang:").grid(row=3, column=0, sticky='w', pady=5)
        self.exam_degree_entry = ttk.Entry(input_frame, width=30)
        self.exam_degree_entry.grid(row=3, column=1, pady=5)
        
        ttk.Button(input_frame, text="Prüfung anlegen", 
                  command=self.add_exam).grid(row=4, column=0, columnspan=2, pady=20)
        
        # Buttons für Aktionen
        button_frame = ttk.LabelFrame(left_column, text="Prüfungsaktionen", padding=10)
        button_frame.pack(side='top', fill='x', padx=5, pady=(5,300))
        
        button_row = ttk.Frame(button_frame)
        button_row.pack(anchor='w')
        
        ttk.Button(button_row, text="Aktualisieren", 
                  command=self.load_exams).pack(side='left', padx=5)
        ttk.Button(button_row, text="Löschen", 
                  command=self.delete_selected_exam).pack(side='left', padx=5)
        ttk.Button(button_row, text="Bearbeiten", 
                  command=self.edit_selected_exam).pack(side='left', padx=5)
        
        # Rechte Spalte: Treeview
        list_frame = ttk.LabelFrame(main_container, text="Vorhandene Prüfungen", padding=10)
        list_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        columns = ('pnr', 'title', 'semester', 'degree')
        self.exam_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.exam_tree.heading('pnr', text='PNr')
        self.exam_tree.heading('title', text='Titel')
        self.exam_tree.heading('semester', text='Semester')
        self.exam_tree.heading('degree', text='Studiengang')
        
        self.exam_tree.column('pnr', width=80)
        self.exam_tree.column('title', width=250)
        self.exam_tree.column('semester', width=80)
        self.exam_tree.column('degree', width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.exam_tree.yview)
        self.exam_tree.configure(yscrollcommand=scrollbar.set)
        
        self.exam_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.exam_content_created = True
    
    def create_student_tab_content(self):
        """Create content for students tab (only called when needed)"""
        if hasattr(self, 'student_content_created') and self.student_content_created:
            return
        
        # Clear existing widgets
        for widget in self.student_tab.winfo_children():
            widget.destroy()
        
        # Hauptcontainer
        main_container = ttk.Frame(self.student_tab)
        main_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Linke Spalte
        left_column = ttk.Frame(main_container)
        left_column.pack(side='left', fill='both', expand=True)
        
        # Eingabefelder
        input_frame = ttk.LabelFrame(left_column, text="Neuen Studenten anlegen", padding=10)
        input_frame.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Matrikelnummer:").grid(row=0, column=0, sticky='w', pady=5)
        self.student_matno_entry = ttk.Entry(input_frame, width=30)
        self.student_matno_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(input_frame, text="Vorname:").grid(row=1, column=0, sticky='w', pady=5)
        self.student_firstname_entry = ttk.Entry(input_frame, width=30)
        self.student_firstname_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(input_frame, text="Nachname:").grid(row=2, column=0, sticky='w', pady=5)
        self.student_lastname_entry = ttk.Entry(input_frame, width=30)
        self.student_lastname_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(input_frame, text="Geburtsdatum (DD-MM-YYYY):").grid(row=3, column=0, sticky='w', pady=5)
        self.student_dob_entry = ttk.Entry(input_frame, width=30)
        self.student_dob_entry.grid(row=3, column=1, pady=5)
        
        ttk.Button(input_frame, text="Student anlegen", 
                  command=self.add_student).grid(row=4, column=0, columnspan=2, pady=20)
        
        # Buttons für Aktionen
        button_frame = ttk.LabelFrame(left_column, text="Studentenaktionen", padding=10)
        button_frame.pack(side='top', fill='x', padx=5, pady=(5, 300))
        
        button_row = ttk.Frame(button_frame)
        button_row.pack(anchor='w')
        
        ttk.Button(button_row, text="Aktualisieren", 
                  command=self.load_students).pack(side='left', padx=5)
        ttk.Button(button_row, text="Löschen", 
                  command=self.delete_selected_student).pack(side='left', padx=5)
        
        # Rechte Spalte: Treeview
        list_frame = ttk.LabelFrame(main_container, text="Vorhandene Studenten", padding=10)
        list_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        columns = ('matno', 'firstname', 'lastname', 'date_of_birth')
        self.student_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.student_tree.heading('matno', text='Matrikelnummer')
        self.student_tree.heading('firstname', text='Vorname')
        self.student_tree.heading('lastname', text='Nachname')
        self.student_tree.heading('date_of_birth', text='Geburtsdatum')
        
        self.student_tree.column('matno', width=120)
        self.student_tree.column('firstname', width=120)
        self.student_tree.column('lastname', width=120)
        self.student_tree.column('date_of_birth', width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        
        self.student_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.student_content_created = True
    
    def create_grade_tab_content(self):
        """Create content for grades tab (only called when needed)"""
        if hasattr(self, 'grade_content_created') and self.grade_content_created:
            return
        
        # Clear existing widgets
        for widget in self.grade_tab.winfo_children():
            widget.destroy()
        
        # Linker Frame: Eingabe
        input_frame = ttk.LabelFrame(self.grade_tab, text="Neue Note eintragen", padding=10)
        input_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Studenten Dropdown
        ttk.Label(input_frame, text="Student:").grid(row=0, column=0, sticky='w', pady=5)
        self.grade_student_var = tk.StringVar()
        self.grade_student_combo = ttk.Combobox(input_frame, textvariable=self.grade_student_var, width=27)
        self.grade_student_combo.grid(row=0, column=1, pady=5)
        ttk.Button(input_frame, text="↻", width=3, 
                  command=self.load_student_combo).grid(row=0, column=2, padx=5)
        
        # Prüfungs Dropdown
        ttk.Label(input_frame, text="Prüfung:").grid(row=1, column=0, sticky='w', pady=5)
        self.grade_exam_var = tk.StringVar()
        self.grade_exam_combo = ttk.Combobox(input_frame, textvariable=self.grade_exam_var, width=27)
        self.grade_exam_combo.grid(row=1, column=1, pady=5)
        ttk.Button(input_frame, text="↻", width=3, 
                  command=self.load_exam_combo).grid(row=1, column=2, padx=5)
        
        ttk.Label(input_frame, text="Note:").grid(row=2, column=0, sticky='w', pady=5)
        self.grade_entry = ttk.Entry(input_frame, width=30)
        self.grade_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(input_frame, text="Prüf.-Datum (DD-MM-YYYY):").grid(row=3, column=0, sticky='w', pady=5)
        self.grade_date_entry = ttk.Entry(input_frame, width=30)
        self.grade_date_entry.insert(0, datetime.now().strftime('%d-%m-%Y'))
        self.grade_date_entry.grid(row=3, column=1, pady=5)
        
        ttk.Button(input_frame, text="Note eintragen", 
                  command=self.add_grade).grid(row=4, column=0, columnspan=3, pady=20)
        
        # Rechter Frame: Notenliste
        list_frame = ttk.LabelFrame(self.grade_tab, text="Noten des ausgewählten Studenten", padding=10)
        list_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        controls_frame = ttk.Frame(list_frame)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(controls_frame, text="Student für Notenanzeige:").grid(row=0, column=0, sticky='w', pady=5)
        
        self.grade_view_student_var = tk.StringVar()
        self.grade_view_student_combo = ttk.Combobox(controls_frame, 
                                                    textvariable=self.grade_view_student_var, 
                                                    width=30)
        self.grade_view_student_combo.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        button_container = ttk.Frame(controls_frame)
        button_container.grid(row=0, column=2, padx=(10, 0), pady=5, sticky='w')
        
        ttk.Button(button_container, text="Noten laden", 
                  command=self.load_grades_for_selected_student).pack(side='left', padx=2)
        ttk.Button(button_container, text="Note löschen", 
                  command=self.delete_selected_grade).pack(side='left', padx=2)
        
        # Treeview für Noten
        columns = ('pnr', 'title', 'grade', 'grade_date')
        self.grade_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        self.grade_tree.heading('pnr', text='PNr')
        self.grade_tree.heading('title', text='Prüfung')
        self.grade_tree.heading('grade', text='Note')
        self.grade_tree.heading('grade_date', text='Datum')
        
        self.grade_tree.column('pnr', width=80)
        self.grade_tree.column('title', width=180)
        self.grade_tree.column('grade', width=80)
        self.grade_tree.column('grade_date', width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.grade_tree.yview)
        self.grade_tree.configure(yscrollcommand=scrollbar.set)
        
        self.grade_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.grade_content_created = True
    
    def create_statistics_tab_content(self):
        """Create content for statistics tab (only called when needed)"""
        if hasattr(self, 'stats_content_created') and self.stats_content_created:
            return
        
        # Clear existing widgets
        for widget in self.statistics_tab.winfo_children():
            widget.destroy()
        
        stats_frame = ttk.LabelFrame(self.statistics_tab, text="Prüfungsstatistiken", padding=20)
        stats_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(stats_frame, text="Prüfung auswählen:").pack(anchor='w', pady=10)
        
        self.stats_exam_var = tk.StringVar()
        self.stats_exam_combo = ttk.Combobox(stats_frame, 
                                            textvariable=self.stats_exam_var, 
                                            width=50)
        self.stats_exam_combo.pack(pady=5)
        
        ttk.Button(stats_frame, text="Statistiken laden", 
                  command=self.load_exam_statistics).pack(pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=10, width=60)
        self.stats_text.pack(pady=10)
        
        self.stats_content_created = True
    
    # ===== EXISTING METHODS (keep as they were) =====
    
    def add_exam(self):
        # Your existing add_exam method
        pnr = self.exam_pnr_entry.get()
        title = self.exam_title_entry.get()
        semester = self.exam_semester_entry.get()
        degree = self.exam_degree_entry.get()
        
        if not pnr or not title:
            messagebox.showwarning("Warnung", "PNr und Titel sind erforderlich!")
            return
        
        try:
            create_exam(pnr, title, semester, degree)
            messagebox.showinfo("Erfolg", "Prüfung erfolgreich angelegt!")
            self.clear_exam_entries()
            self.load_exams()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Anlegen: {e}")
    
    def load_exams(self):
        # Your existing load_exams method
        for item in self.exam_tree.get_children():
            self.exam_tree.delete(item)
        
        exams = get_all_exams()
        for exam in exams:
            self.exam_tree.insert('', 'end', values=exam)
    
    def delete_selected_exam(self):
        # Your existing delete_selected_exam method
        selected = self.exam_tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Prüfung aus!")
            return
        
        item = self.exam_tree.item(selected[0])
        pnr = item['values'][0]
        
        if messagebox.askyesno("Bestätigen", f"Prüfung {pnr} wirklich löschen?"):
            try:
                delete_exam(pnr)
                messagebox.showinfo("Erfolg", "Prüfung gelöscht!")
                self.load_exams()
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Löschen: {e}")
    
    def edit_selected_exam(self):
        # Your existing edit_selected_exam method
        selected = self.exam_tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Prüfung aus!")
            return
        
        item = self.exam_tree.item(selected[0])
        values = item['values']
        self.open_edit_exam_dialog(values)
    
    def open_edit_exam_dialog(self, values):
        # Your existing open_edit_exam_dialog method
        dialog = tk.Toplevel(self.root)
        dialog.title("Prüfung bearbeiten")
        dialog.geometry("400x300")
        
        pnr, title, semester, degree = values
        
        ttk.Label(dialog, text="PNr:").pack(pady=5)
        pnr_label = ttk.Label(dialog, text=pnr)
        pnr_label.pack(pady=5)
        
        ttk.Label(dialog, text="Titel:").pack(pady=5)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.insert(0, title)
        title_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Semester:").pack(pady=5)
        semester_entry = ttk.Entry(dialog, width=40)
        semester_entry.insert(0, semester)
        semester_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Studiengang:").pack(pady=5)
        degree_entry = ttk.Entry(dialog, width=40)
        degree_entry.insert(0, degree)
        degree_entry.pack(pady=5)
        
        def save_changes():
            new_title = title_entry.get()
            new_semester = semester_entry.get()
            new_degree = degree_entry.get()
            
            try:
                update_exam(pnr, new_title, new_semester, new_degree)
                messagebox.showinfo("Erfolg", "Prüfung aktualisiert!")
                dialog.destroy()
                self.load_exams()
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Aktualisieren: {e}")
        
        ttk.Button(dialog, text="Speichern", command=save_changes).pack(pady=20)
    
    def clear_exam_entries(self):
        self.exam_pnr_entry.delete(0, tk.END)
        self.exam_title_entry.delete(0, tk.END)
        self.exam_semester_entry.delete(0, tk.END)
        self.exam_degree_entry.delete(0, tk.END)
    
    def add_student(self):
        # Your existing add_student method
        matno = self.student_matno_entry.get()
        firstname = self.student_firstname_entry.get()
        lastname = self.student_lastname_entry.get()
        dob = self.student_dob_entry.get()
        
        if not matno or not firstname or not lastname:
            messagebox.showwarning("Warnung", "Matrikelnummer, Vorname und Nachname sind erforderlich!")
            return
        
        try:
            datetime.strptime(dob, '%d-%m-%Y')
            create_student(matno, firstname, lastname, dob)
            messagebox.showinfo("Erfolg", "Student erfolgreich angelegt!")
            self.clear_student_entries()
            self.load_students()
        except ValueError:
            messagebox.showerror("Fehler", "Ungültiges Datumsformat! Verwenden Sie DD-MM-YYYY")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Anlegen: {e}")
    
    def load_students(self):
        # Your existing load_students method
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        students = get_all_students()
        for student in students:
            self.student_tree.insert('', 'end', values=student)
    
    def delete_selected_student(self):
        # Your existing delete_selected_student method
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wählen Sie einen Studenten aus!")
            return
        
        item = self.student_tree.item(selected[0])
        matno = item['values'][0]
        name = f"{item['values'][1]} {item['values'][2]}"
        
        if messagebox.askyesno("Bestätigen", f"Student {name} ({matno}) wirklich löschen?"):
            try:
                delete_student(matno)
                messagebox.showinfo("Erfolg", "Student gelöscht!")
                self.load_students()
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Löschen: {e}")
    
    def clear_student_entries(self):
        self.student_matno_entry.delete(0, tk.END)
        self.student_firstname_entry.delete(0, tk.END)
        self.student_lastname_entry.delete(0, tk.END)
        self.student_dob_entry.delete(0, tk.END)
    
    def load_student_combo(self):
        # Your existing load_student_combo method
        students = get_all_students()
        student_list = [f"{s[0]} - {s[1]} {s[2]}" for s in students]
        self.grade_student_combo['values'] = student_list
        if student_list:
            self.grade_student_combo.set(student_list[0])
    
    def load_exam_combo(self):
        # Your existing load_exam_combo method
        exams = get_all_exams()
        exam_list = [f"{e[0]} - {e[1]}" for e in exams]
        self.grade_exam_combo['values'] = exam_list
        if exam_list:
            self.grade_exam_combo.set(exam_list[0])
    
    def load_students_for_grade_view(self):
        # Your existing load_students_for_grade_view method
        students = get_all_students()
        student_list = [f"{s[0]} - {s[1]} {s[2]}" for s in students]
        self.grade_view_student_combo['values'] = student_list
        if student_list:
            self.grade_view_student_combo.set(student_list[0])
    
    def add_grade(self):
        # Your existing add_grade method
        student_str = self.grade_student_var.get()
        if not student_str:
            messagebox.showwarning("Warnung", "Bitte wählen Sie einen Studenten!")
            return
        
        matno = student_str.split(' - ')[0]
        
        exam_str = self.grade_exam_var.get()
        if not exam_str:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Prüfung!")
            return
        
        pnr = exam_str.split(' - ')[0]
        
        grade = self.grade_entry.get()
        grade_date = self.grade_date_entry.get()
        
        if not grade:
            messagebox.showwarning("Warnung", "Bitte geben Sie eine Note ein!")
            return
        
        try:
            grade_float = float(grade)
            if grade_float < 1.0 or grade_float > 5.0:
                raise ValueError("Note muss zwischen 1.0 und 5.0 liegen")
            
            datetime.strptime(grade_date, '%d-%m-%Y')
            
            create_grade(matno, pnr, grade_float, grade_date)
            messagebox.showinfo("Erfolg", "Note erfolgreich eingetragen!")
            self.grade_entry.delete(0, tk.END)
            self.load_grades_for_selected_student()
        except ValueError as e:
            messagebox.showerror("Fehler", f"Ungültige Eingabe: {e}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Eintragen: {e}")
    
    def load_grades_for_selected_student(self):
        # Your existing load_grades_for_selected_student method
        student_str = self.grade_view_student_var.get()
        if not student_str:
            return
        
        matno = student_str.split(' - ')[0]
        
        for item in self.grade_tree.get_children():
            self.grade_tree.delete(item)
        
        grades = get_grades_for_student(matno)
        for grade in grades:
            self.grade_tree.insert('', 'end', values=grade)
    
    def delete_selected_grade(self):
        # Your existing delete_selected_grade method
        selected = self.grade_tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Note aus!")
            return
        
        item = self.grade_tree.item(selected[0])
        pnr = item['values'][0]
        
        student_str = self.grade_view_student_var.get()
        matno = student_str.split(' - ')[0]
        
        exam_title = item['values'][1]
        
        if messagebox.askyesno("Bestätigen", f"Note für '{exam_title}' wirklich löschen?"):
            try:
                delete_grade(matno, pnr)
                messagebox.showinfo("Erfolg", "Note gelöscht!")
                self.load_grades_for_selected_student()
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Löschen: {e}")
    
    def load_stats_exam_combo(self):
        # Your existing load_stats_exam_combo method
        exams = get_all_exams()
        exam_list = [f"{e[0]} - {e[1]}" for e in exams]
        self.stats_exam_combo['values'] = exam_list
        if exam_list:
            self.stats_exam_combo.set(exam_list[0])
    
    def load_exam_statistics(self):
        # Your existing load_exam_statistics method
        exam_str = self.stats_exam_var.get()
        if not exam_str:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Prüfung!")
            return
        
        pnr = exam_str.split(' - ')[0]
        
        try:
            stats = get_exam_statistics(pnr)
            
            self.stats_text.delete(1.0, tk.END)
            
            if stats[0] is None:
                self.stats_text.insert(1.0, "Für diese Prüfung liegen noch keine Noten vor.")
            else:
                result_text = f"Statistik für Prüfung: {exam_str}\n"
                result_text += "=" * 40 + "\n\n"
                result_text += f"Durchschnittsnote: {stats[0]:.2f}\n"
                result_text += f"Beste Note: {stats[1]:.2f}\n"
                result_text += f"Schlechteste Note: {stats[2]:.2f}\n"
                result_text += f"Anzahl Teilnehmer: {stats[3]}\n"
                
                self.stats_text.insert(1.0, result_text)
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Statistiken: {e}")


def main():
    root = tk.Tk()
    app = ExamManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()