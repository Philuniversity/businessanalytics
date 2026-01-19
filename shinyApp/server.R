function(input, output, session) {

  # =========================================================
  # REAKTIVE DROPDOWN-DATEN
  # =========================================================
  students_reactive <- reactive({
    dbGetQuery(
      con,
      "SELECT matno, firstname, lastname FROM students ORDER BY lastname"
    )
  })

  exams_reactive <- reactive({
    dbGetQuery(
      con,
      "SELECT pnr, title FROM exams ORDER BY title"
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

  observe({
    sem_df <- dbGetQuery(con, "SELECT DISTINCT semester FROM exams ORDER BY semester")
    updateSelectInput(
      session,
      "selected_semester",
      choices = sem_df$semester
    )
  })

  observe({
    deg_df <- dbGetQuery(con, "SELECT DISTINCT degree FROM exams ORDER BY degree")
    updateSelectInput(
      session,
      "selected_degree",
      choices = deg_df$degree
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
        students.matno,
        students.firstname,
        students.lastname,
        AVG(grades.grade) AS gpa
      FROM students
      JOIN grades ON students.matno = grades.matno
      GROUP BY
        students.matno,
        students.firstname,
        students.lastname
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
      SELECT exams.title, exams.semester, grades.grade,
             TO_CHAR(grades.grade_date, 'YYYY-MM-DD') AS grade_date
      FROM grades
      JOIN exams ON grades.pnr = exams.pnr
      WHERE grades.matno = $1
      ORDER BY exams.title
      ",
      params = list(input$selected_student)
    )
  })

  output$student_avg <- renderText({
    req(input$selected_student)

    res <- dbGetQuery(
      con,
      "SELECT ROUND(AVG(grade), 2) AS avg_grade FROM grades WHERE matno = $1",
      params = list(input$selected_student)
    )

    if (is.na(res$avg_grade)) "Keine Noten vorhanden" else res$avg_grade
  })

  # =========================================================
  # EXAM TAB
  # =========================================================
  output$exam_grades_table <- renderTable({
    req(input$selected_exam)

    df <- dbGetQuery(
      con,
      "
      SELECT students.firstname, students.lastname, grades.grade
      FROM grades
      JOIN students ON grades.matno = students.matno
      WHERE grades.pnr = $1
      ORDER BY grades.grade
      ",
      params = list(input$selected_exam)
    )

    if (nrow(df) == 0) {
      return(data.frame(
        firstname = "",
        lastname  = "Keine Noten vorhanden",
        grade     = NA,
        stringsAsFactors = FALSE
      ))
    }

    gpa_row <- data.frame(
      firstname = "",
      lastname  = "GPA",
      grade     = round(mean(df$grade, na.rm = TRUE), 2),
      stringsAsFactors = FALSE
    )

    rbind(df, gpa_row)
  })

  output$exam_grades_plot <- renderPlot({
    req(input$selected_exam)

    df <- dbGetQuery(
      con,
      "
      SELECT grade, COUNT(*) AS count
      FROM grades
      WHERE pnr = $1
      GROUP BY grade
      ORDER BY grade
      ",
      params = list(input$selected_exam)
    )

    ggplot(df, aes(x = grade, y = count)) +
      geom_col(width = 0.14, fill = "#337ab7") +
      scale_x_continuous(breaks = seq(1, 5, by = 0.5)) +
      coord_cartesian(xlim = c(1, 5)) +
      theme_minimal(base_size = 14)
  })

  # =========================================================
  # STATISTIK TAB
  # =========================================================
  output$all_gpa_table <- renderTable({
    df <- gpa_df()
    df$gpa <- round(df$gpa, 2)
    df <- df[order(df$gpa), ]

    if (nrow(df) == 0) return(df)

    median_row <- data.frame(
      matno = NA,
      firstname = "",
      lastname = "Median",
      gpa = round(median(df$gpa, na.rm = TRUE), 2),
      stringsAsFactors = FALSE
    )

    sd_row <- data.frame(
      matno = NA,
      firstname = "",
      lastname = "Std. Deviation",
      gpa = round(sd(df$gpa, na.rm = TRUE), 2),
      stringsAsFactors = FALSE
    )

    rbind(df, median_row, sd_row)
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
      scale_x_continuous(breaks = seq(1, 5, by = 0.2)) +
      coord_cartesian(xlim = c(1, 5)) +
      labs(
        x = "Durchschnittsnote",
        y = "Anzahl Studierender"
      ) +
      theme_minimal(base_size = 14)
  })

  output$gpa_semester_degree_table <- renderTable({
    req(input$selected_semester, input$selected_degree)

    gpa <- dbGetQuery(
      con,
      "
      SELECT ROUND(AVG(g.grade)::numeric, 2) AS gpa
      FROM grades g
      JOIN exams e ON g.pnr = e.pnr
      WHERE e.semester = $1
        AND e.degree = $2
      ",
      params = list(
        as.integer(input$selected_semester),
        input$selected_degree
      )
    )

    data.frame(
      semester = as.integer(input$selected_semester),
      degree = input$selected_degree,
      gpa = gpa$gpa,
      stringsAsFactors = FALSE
    )
  })

  # =========================================================
  # DB VERBINDUNG SCHLIESSEN
  # =========================================================
  session$onSessionEnded(function() {
    dbDisconnect(con)
  })
}
