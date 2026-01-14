function(input, output, session) {

  # =========================================================
  # REAKTIVE DROPDOWN-DATEN
  # =========================================================
  students_reactive <- reactive({
    dbGetQuery(
      con,
      "SELECT matno, firstname, lastname FROM student ORDER BY lastname"
    )
  })

  exams_reactive <- reactive({
    dbGetQuery(
      con,
      "SELECT pnr, title FROM exam ORDER BY title"
    )
  })

  observe({
    students <- students_reactive()
    updateSelectInput(
      session,
      "selected_student",
      choices = setNames(
        students$matno,
        paste(students$firstname, students$lastname)
      )
    )
  })

  observe({
    exams <- exams_reactive()
    updateSelectInput(
      session,
      "selected_exam",
      choices = setNames(
        exams$pnr,
        exams$title
      )
    )
  })

  # =========================================================
  # AUTOMATISCHER TAB-WECHSEL
  # =========================================================
  observeEvent(input$selected_student, {
    updateTabsetPanel(session, "main_tabs", selected = "Student")
  })

  observeEvent(input$selected_exam, {
    updateTabsetPanel(session, "main_tabs", selected = "Exam")
  })

  # =========================================================
  # ZENTRALE GPA-DATEN
  # =========================================================
  get_all_gpa <- function(con) {
    dbGetQuery(
      con,
      "
      SELECT
        student.matno,
        student.firstname,
        student.lastname,
        student.semester,
        student.degree,
        AVG(grade.grade) AS gpa
      FROM student
      JOIN grade ON student.matno = grade.matno
      GROUP BY
        student.matno,
        student.firstname,
        student.lastname,
        student.semester,
        student.degree
      "
    )
  }

  gpa_df <- reactive({ get_all_gpa(con) })

  # =========================================================
  # STUDENT TAB
  # =========================================================
  output$student_grades_table <- renderTable({
    req(input$selected_student)

    dbGetQuery(
      con,
      "
      SELECT exam.title, exam.semester, grade.grade,
             TO_CHAR(grade.grade_date, 'YYYY-MM-DD') AS grade_date
      FROM grade
      JOIN exam ON grade.pnr = exam.pnr
      WHERE grade.matno = $1
      ORDER BY exam.title
      ",
      params = list(input$selected_student)
    )
  })

  output$student_avg <- renderText({
    req(input$selected_student)

    res <- dbGetQuery(
      con,
      "SELECT ROUND(AVG(grade), 2) AS avg_grade FROM grade WHERE matno = $1",
      params = list(input$selected_student)
    )

    if (is.na(res$avg_grade)) "Keine Noten vorhanden" else res$avg_grade
  })

  # =========================================================
  # EXAM TAB
  # =========================================================
  output$exam_grades_table <- renderTable({
    req(input$selected_exam)

    dbGetQuery(
      con,
      "
      SELECT student.firstname, student.lastname, student.semester, grade.grade
      FROM grade
      JOIN student ON grade.matno = student.matno
      WHERE grade.pnr = $1
      ORDER BY grade.grade
      ",
      params = list(input$selected_exam)
    )
  })

  output$exam_grades_plot <- renderPlot({
    req(input$selected_exam)

    df <- dbGetQuery(
      con,
      "
      SELECT grade, COUNT(*) AS count
      FROM grade
      WHERE pnr = $1
      GROUP BY grade
      ORDER BY grade
      ",
      params = list(input$selected_exam)
    )

    ggplot(df, aes(x = grade, y = count)) +
      geom_col(width = 0.14, fill = "#337ab7") +
      scale_x_continuous(limits = c(1, 5), breaks = seq(1, 5, by = 0.5)) +
      theme_minimal(base_size = 14)
  })

  # =========================================================
  # STATISTIK TAB
  # =========================================================
  output$all_gpa_table <- renderTable({
    df <- gpa_df()
    df$gpa <- round(df$gpa, 2)
    df
  })

  output$all_gpa_plot <- renderPlot({
  df <- gpa_df()
  df$gpa <- round(df$gpa, 2)

  ggplot(df, aes(x = gpa)) +
    geom_histogram(
      binwidth = 0.1,
      boundary = 1,
      closed = "left",
      fill = "#337ab7"
    ) +
    scale_x_continuous(
      breaks = seq(1, 5, by = 0.2)
    ) +
    coord_cartesian(xlim = c(1, 5)) +
    labs(
      x = "Durchschnittsnote",
      y = "Anzahl Studierender"
    ) +
    theme_minimal(base_size = 14)
})

  # =========================================================
  # DB VERBINDUNG SCHLIESSEN
  # =========================================================
  session$onSessionEnded(function() {
    dbDisconnect(con)
  })
}
