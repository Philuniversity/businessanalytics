README – BA-Sys-Dev Projekt (Python Backend)
Projektübersicht
Dieses Projekt bildet die Backend-Komponente eines größeren Systems zur Verwaltung von Studierenden, Prüfungen und vergebenen Noten.
Es ist Teil des Moduls Business Analytics System Development und dient als Grundlage für:
•	das Python-Frontend (tkinter),
•	das R-Shiny-Dashboard zur Analyse,
•	sowie die Präsentation des Gesamtsystems.
Der Fokus dieser Komponente liegt vollständig auf:
1.	Einrichtung der PostgreSQL-Datenbank
2.	Erstellung der Datenbanktabellen
3.	Verwaltung und Bereitstellung von Trainingsdaten
4.	Entwicklung der Backend-Logik (CRUD & Abfragen)
Dieses Backend bildet somit das Fundament für die Arbeit der anderen Gruppenmitglieder.
 
Datenbankmodell
Die Datenbank examdb basiert auf drei zentralen Tabellen:
1. student
Feld	Typ
matno (PK)	VARCHAR
firstname	VARCHAR
lastname	VARCHAR
date_of_birth	DATE
semester	INTEGER
degree	VARCHAR
2. exam
Feld	Typ
pnr (PK)	VARCHAR
title	VARCHAR
exam_date	DATE
semester	INTEGER
degree	VARCHAR
3. grade
Feld	Typ	Beschreibung
matno (FK)	VARCHAR	Verweis auf student
pnr (FK)	VARCHAR	Verweis auf exam
grade	NUMERIC	Note (1.0–5.0)
grade_date	DATE	Datum der Bewertung
Die Tabelle grade bildet eine klassische n:m-Beziehung ab:
Eine Studierender kann mehrere Prüfungen haben, und eine Prüfung kann mehreren Studierenden zugeordnet sein.




Projektstruktur
ba-backend/
│
├── backend/
│   ├── __init__.py
│   ├── database.py            → Verbindung zur PostgreSQL-Datenbank
│   ├── student_service.py     → CRUD für Studierende
│   ├── exam_service.py        → CRUD für Prüfungen
│   ├── grade_service.py       → CRUD für Noten
│   ├── main.py                → Test- und Demonstrationsskript
│
├── venv/                      → Virtuelle Python-Umgebung (lokal)
│
└── README.md                  → Diese Dokumentation
 
Wesentliche Python-Komponenten
 database.py
•	Herstellung der DB-Verbindung über psycopg2
•	Zentraler Einstiegspunkt für alle SQL-Operationen
 student_service.py
•	Anlegen, Lesen, Aktualisieren und Löschen von Studierenden
•	Rückgabe strukturierter Python-Objekte für die spätere GUI-/Analyse-Ebene
 exam_service.py
•	Verwaltung der Prüfungen
•	Fachlogik getrennt von der Datenhaltung
 grade_service.py
•	Einfügen und Anpassen von Noten
•	Lesen der Noten eines bestimmten Studierenden oder einer Prüfung
•	Berechnung statistischer Kennzahlen
 main.py
•	Dient ausschließlich als Testumgebung
•	Führt Beispiele für CRUD-Operationen aus
•	Erleichtert das Debugging für frontend- und analysebezogene Teammitglieder

Trainingsdaten
Zur Demonstration und Testbarkeit wurden realistische Datensätze erzeugt:
•	5 Beispielstudierende
•	mehrere Prüfungen aus verschiedenen Studiengängen
•	Notenbeispiele inklusive unterschiedlicher Prüfungsdaten
Diese Daten ermöglichen:
•	vollständige Funktionalität der tkinter-GUI
•	statistische Auswertungen in R
•	nachvollziehbare Präsentationen
 
Technische Einrichtung
1. Erforderliche Software
•	Python 3.14.x
•	PostgreSQL 18
•	pgAdmin 4
•	psycopg2-binary (Python DB-Adapter)
2. Virtuelle Umgebung aktivieren
Im Projektverzeichnis:
venv\Scripts\activate
3. Notwendige Pakete installieren
pip install psycopg2-binary
4. main.py ausführen
python -m backend.main

Wichtige Designentscheidungen
✔ Trennung von Datenzugriff und Fachlogik
Die Datenbankoperationen sind klar getrennt von der eigentlichen Programmlogik. Dadurch können:
•	tkinter-Dialoge,
•	R-Shiny Anwendungen,
•	Präsentationsskripte
unabhängig vom Backend entwickelt werden.
✔ Kapselung in Services
Statt alles in eine Datei zu schreiben, sind die Funktionen logisch gruppiert:
•	Student-related → student_service.py
•	Exams → exam_service.py
•	Grades → grade_service.py
Dies schafft Übersichtlichkeit und erleichtert die Weiterentwicklung im Team.
✔ Einfach erweiterbar
Für spätere Erweiterungen (z. B. API, Validierung, Exceptions, Logging) ist das Projekt leicht anpassbar.

Wie geht es im Gesamtprojekt weiter?
Das Backend dient als Grundlage für:
1. Python-Frontend (tkinter)
•	Drei Dialogfenster zur Verwaltung:
o	Studierende
o	Prüfungen
o	Noten
•	Direkter Zugriff auf die Service-Funktionen
2. R-Analyse / Dashboard
•	Auslesen der PostgreSQL-Daten
•	Berechnung von:
o	Durchschnittsnoten
o	Statistikkennzahlen
o	Semester- und Degree-Auswertungen
•	Grafische Darstellung (z. B. Balken- und Boxplots)

Zusammenfassung
Dieses Backend bildet das vollständige Fundament für das BA-Sys-Dev-Projekt.
Es stellt alle notwendigen Funktionen bereit, um:
•	Daten in PostgreSQL zu verwalten,
•	Trainingsdaten bereitzustellen,
•	das GUI und das Dashboard aufzubauen,
•	und ein durchgängiges System von Datenerfassung bis Analyse zu ermöglichen.
Das System ist modular aufgebaut, leicht verständlich und für alle Teammitglieder direkt weiterverwendbar.

