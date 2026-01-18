import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


from backend.exam_service import create_exam, get_all_exams, update_exam, delete_exam
from backend.student_service import create_student, get_all_students, update_student, delete_student
from backend.grade_service import create_grade, get_grades_for_student, get_exam_statistics, update_grade, delete_grade


class ExamManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prüfungsverwaltungssystem")
        self.root.geometry("1100x700")
        
        # Notebook System für alle Tabs für bessere Orgnatisation
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tabs erstellen
        self.create_exam_tab()
        self.create_student_tab()
        self.create_grade_tab()
        self.create_statistics_tab()
        
    # ===== TAB 1: Prüfungen verwalten =====
# ===== TAB 1: Prüfungen verwalten =====
    def create_exam_tab(self):
        exam_tab = ttk.Frame(self.notebook)
        self.notebook.add(exam_tab, text="Prüfungen")
        
        # Hauptcontainer mit 2 Spalten
        main_container = ttk.Frame(exam_tab)
        main_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Linke Spalte mit 2 vertikalen Frames
        left_column = ttk.Frame(main_container)
        left_column.pack(side='left', fill='both', expand=True)
        
        # OBERER Frame: Eingabefelder
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
        
        # UNTERER Frame: Buttons für Aktionen (links unten)
        button_frame = ttk.LabelFrame(left_column, text="Prüfungsaktionen", padding=10)
        button_frame.pack(side='top', fill='x', padx=5, pady=(5,300))
        
        # Buttons in einer horizontalen Reihe
        button_row = ttk.Frame(button_frame)
        button_row.pack(anchor='w')  # Links ausrichten
        
        ttk.Button(button_row, text="Aktualisieren", 
                command=self.load_exams).pack(side='left', padx=5)
        ttk.Button(button_row, text="Löschen", 
                command=self.delete_selected_exam).pack(side='left', padx=5)
        ttk.Button(button_row, text="Bearbeiten", 
                command=self.edit_selected_exam).pack(side='left', padx=5)
        
        # Rechte Spalte: Treeview (größer)
        list_frame = ttk.LabelFrame(main_container, text="Vorhandene Prüfungen", padding=10)
        list_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Treeview, für bessere Sichtbarkeit
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
        
        # Initiale Ladung
        self.load_exams()
    
    def add_exam(self):
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
        # Treeview leeren
        for item in self.exam_tree.get_children():
            self.exam_tree.delete(item)
        
        # Daten laden und einfügen
        exams = get_all_exams()
        for exam in exams:
            self.exam_tree.insert('', 'end', values=exam)
    
    def delete_selected_exam(self):
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
        selected = self.exam_tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Prüfung aus!")
            return
        
        item = self.exam_tree.item(selected[0])
        values = item['values']
        
        # Bearbeitungsdialog öffnen
        self.open_edit_exam_dialog(values)
    
    def open_edit_exam_dialog(self, values):
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
    

   # ===== TAB 2: Studenten verwalten =====
    def create_student_tab(self):
        student_tab = ttk.Frame(self.notebook)
        self.notebook.add(student_tab, text="Studenten")
        
        # Hauptcontainer mit 2 Spalten
        main_container = ttk.Frame(student_tab)
        main_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Linke Spalte mit 2 vertikalen Frames
        left_column = ttk.Frame(main_container)
        left_column.pack(side='left', fill='both', expand=True)
        
        # OBERER Frame: Eingabefelder
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
        
        # UNTERER Frame: Buttons für Aktionen (links unten)
        button_frame = ttk.LabelFrame(left_column, text="Studentenaktionen", padding=10)
        button_frame.pack(side='top', fill='x', padx=5, pady=(5, 300))
        
        # Buttons in einer horizontalen Reihe
        button_row = ttk.Frame(button_frame)
        button_row.pack(anchor='w')  # Links ausrichten
        
        ttk.Button(button_row, text="Aktualisieren", 
                command=self.load_students).pack(side='left', padx=5)
        ttk.Button(button_row, text="Löschen", 
                command=self.delete_selected_student).pack(side='left', padx=5)
        
        # Rechte Spalte: Treeview (größer)
        list_frame = ttk.LabelFrame(main_container, text="Vorhandene Studenten", padding=10)
        list_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Treeview für Studenten
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
        
        # Initiale Ladung
        self.load_students()
        
    def add_student(self):
        matno = self.student_matno_entry.get()
        firstname = self.student_firstname_entry.get()
        lastname = self.student_lastname_entry.get()
        dob = self.student_dob_entry.get()
        
        if not matno or not firstname or not lastname:
            messagebox.showwarning("Warnung", "Matrikelnummer, Vorname und Nachname sind erforderlich!")
            return
        
        try:
            # Datumsvalidierung
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
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        students = get_all_students()
        for student in students:
            self.student_tree.insert('', 'end', values=student)
    
    def delete_selected_student(self):
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
    
    # ===== TAB 3: Noten verwalten =====

    def create_grade_tab(self):
        grade_tab = ttk.Frame(self.notebook)
        self.notebook.add(grade_tab, text="Noten")
        
        # Linker Frame: Eingabe
        input_frame = ttk.LabelFrame(grade_tab, text="Neue Note eintragen", padding=10)
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
        
        # Rechter Frame: Notenliste für ausgewählten Studenten
        list_frame = ttk.LabelFrame(grade_tab, text="Noten des ausgewählten Studenten", padding=10)
        list_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Studentenauswahl und Buttons Container
        controls_frame = ttk.Frame(list_frame)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        # Studentenauswahl für Notenanzeige
        ttk.Label(controls_frame, text="Student für Notenanzeige:").grid(row=0, column=0, sticky='w', pady=5)
        
        self.grade_view_student_var = tk.StringVar()
        self.grade_view_student_combo = ttk.Combobox(controls_frame, 
                                                    textvariable=self.grade_view_student_var, 
                                                    width=30)
        self.grade_view_student_combo.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Button Container für "Noten laden" und "Note löschen"
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
        
        # Combos initial laden
        self.load_student_combo()
        self.load_exam_combo()
        self.load_students_for_grade_view()
    
    def load_student_combo(self):
        students = get_all_students()
        student_list = [f"{s[0]} - {s[1]} {s[2]}" for s in students]
        self.grade_student_combo['values'] = student_list
        if student_list:
            self.grade_student_combo.set(student_list[0])
    
    def load_exam_combo(self):
        exams = get_all_exams()
        exam_list = [f"{e[0]} - {e[1]}" for e in exams]
        self.grade_exam_combo['values'] = exam_list
        if exam_list:
            self.grade_exam_combo.set(exam_list[0])
    
    def load_students_for_grade_view(self):
        students = get_all_students()
        student_list = [f"{s[0]} - {s[1]} {s[2]}" for s in students]
        self.grade_view_student_combo['values'] = student_list
        if student_list:
            self.grade_view_student_combo.set(student_list[0])
            self.load_grades_for_selected_student()
    
    def add_grade(self):
        # Student aus Combo extrahieren
        student_str = self.grade_student_var.get()
        if not student_str:
            messagebox.showwarning("Warnung", "Bitte wählen Sie einen Studenten!")
            return
        
        matno = student_str.split(' - ')[0]
        
        # Prüfung aus Combo extrahieren
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
        student_str = self.grade_view_student_var.get()
        if not student_str:
            return
        
        matno = student_str.split(' - ')[0]
        
        # Treeview leeren
        for item in self.grade_tree.get_children():
            self.grade_tree.delete(item)
        
        # Noten laden
        grades = get_grades_for_student(matno)
        for grade in grades:
            self.grade_tree.insert('', 'end', values=grade)
    
    def delete_selected_grade(self):
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
    
    # ===== TAB 4: Statistiken =====
    def create_statistics_tab(self):
        stats_tab = ttk.Frame(self.notebook)
        self.notebook.add(stats_tab, text="Statistiken")
        
        # Prüfungsstatistiken
        stats_frame = ttk.LabelFrame(stats_tab, text="Prüfungsstatistiken", padding=20)
        stats_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ttk.Label(stats_frame, text="Prüfung auswählen:").pack(anchor='w', pady=10)
        
        self.stats_exam_var = tk.StringVar()
        self.stats_exam_combo = ttk.Combobox(stats_frame, 
                                            textvariable=self.stats_exam_var, 
                                            width=50)
        self.stats_exam_combo.pack(pady=5)
        
        ttk.Button(stats_frame, text="Statistiken laden", 
                  command=self.load_exam_statistics).pack(pady=10)
        
        # Ergebnisse anzeigen
        self.stats_text = tk.Text(stats_frame, height=10, width=60)
        self.stats_text.pack(pady=10)
        
        # Combobox laden
        self.load_stats_exam_combo()
    
    def load_stats_exam_combo(self):
        exams = get_all_exams()
        exam_list = [f"{e[0]} - {e[1]}" for e in exams]
        self.stats_exam_combo['values'] = exam_list
        if exam_list:
            self.stats_exam_combo.set(exam_list[0])
    
    def load_exam_statistics(self):
        exam_str = self.stats_exam_var.get()
        if not exam_str:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Prüfung!")
            return
        
        pnr = exam_str.split(' - ')[0]
        
        try:
            stats = get_exam_statistics(pnr)
            
            self.stats_text.delete(1.0, tk.END)
            
            if stats[0] is None:  # Keine Noten vorhanden
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