from backend.student_service import get_all_students, update_student
from backend.exam_service import get_all_exams
from backend.grade_service import get_grades_for_student, get_exam_statistics, update_grade


def main():
    print("Alle Studenten:")
    for row in get_all_students():
        print(row)

    print("\nAlle Prüfungen:")
    for row in get_all_exams():
        print(row)

    print("\nNoten von Student 1002:")
    for row in get_grades_for_student("1002"):
        print(row)

    print("\nStatistik für BA101:")
    print(get_exam_statistics("BA101"))

    # Beispiel-Update (optional)
    print("\nSetze Note von 1002 in BA101 auf 1.3 ...")
    update_grade("1002", "BA101", grade=1.3)
    print(get_grades_for_student("1002"))

    print("\nÄndere Nachnamen von Student 1003 auf 'Neu' ...")
    update_student("1003", lastname="Neu")
    print(get_all_students())

    print("\nFertig – Services funktionieren.")


if __name__ == "__main__":
    main()
