library(shiny)

ui <- fluidPage(

  titlePanel("Student Exam Analytics Dashboard"),

  # =========================================================
  # FILTERLEISTE
  # =========================================================
  fluidRow(
    column(
      width = 12,
      tags$div(
        style = "
          display: flex;
          align-items: center;
          gap: 20px;
          padding: 10px 15px;
          margin-bottom: 10px;
          border-bottom: 1px solid #ddd;
        ",

        tags$strong("Filteroptionen:"),

        tags$label("Student:", style = "margin: 0;"),
        selectInput(
          "selected_student",
          NULL,
          choices = NULL,
          width = "250px"
        ),

        tags$label("Exam:", style = "margin: 0;"),
        selectInput(
          "selected_exam",
          NULL,
          choices = NULL,
          width = "250px"
        )
      )
    )
  ),

  # =========================================================
  # TABS
  # =========================================================
  fluidRow(
    column(
      width = 12,

      tabsetPanel(
        id = "main_tabs",

        tabPanel(
          "Student",
          h3("Alle Noten eines Studenten"),
          tableOutput("student_grades_table"),
          h4("Durchschnittsnote"),
          textOutput("student_avg")
        ),

        tabPanel(
          "Exam",
          h3("Exam-Ergebnisse"),
          fluidRow(
            column(
              width = 6,
              h4("Alle Noten des Exams"),
              tableOutput("exam_grades_table")
            ),
            column(
              width = 6,
              style = "padding-left: 5px;",
              h4("Notenverteilung"),
              plotOutput("exam_grades_plot")
            )
          )
        ),

        tabPanel(
          "Statistik",
          h3("Statistikübersicht"),
          fluidRow(
            column(
              width = 6,
              h4("Durchschnittsnoten aller Studenten"),
              tableOutput("all_gpa_table")
            ),
            column(
              width = 6,
              style = "padding-left: 5px;",
              h4("Verteilung der Durchschnittsnoten"),
              plotOutput("all_gpa_plot")
            )
          )
        ),

        tabPanel(
          "Programme",
          h3("Durchschnittsnoten pro Semester und Studiengang"),
          fluidRow(
            column(
              width = 12,
              tags$div(
                style = "
                  display: flex;
                  align-items: center;
                  gap: 20px;
                  padding: 10px 15px;
                  margin-bottom: 10px;
                  border-bottom: 1px solid #ddd;
                ",

                tags$strong("Filteroptionen:"),

                tags$label("Semester:", style = "margin: 0;"),
                selectInput(
                  "selected_semester",
                  NULL,
                  choices = NULL,
                  width = "250px"
                ),

                tags$label("Studiengang:", style = "margin: 0;"),
                selectInput(
                  "selected_degree",
                  NULL,
                  choices = NULL,
                  width = "250px"
                )
              )
            )
          ),
          h4("Grade Point Average (GPA)"),
          tableOutput("gpa_semester_degree_table")
        )
      )
    )
  )
)
