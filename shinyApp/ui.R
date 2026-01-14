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
        )
      )
    )
  )
)




#library(shiny)

#ui <- fluidPage(
#  
#  titlePanel("Student Exam Analytics Dashboard"),
#  
#  sidebarLayout(
#    
#    sidebarPanel(
#      h3("Filter"),
#      
#      selectInput(
#        "selected_student",
#        "Wähle einen Studenten:",
#        choices = student_choices
#      ),
#      
#      selectInput(
#        "selected_exam",
#        "Wähle ein Exam:",
#        choices = exam_choices
#      )
#    ),
#    
#    mainPanel(
#      tabsetPanel(
#        
#        tabPanel("Student",
#                 h3("Alle Noten eines Studenten"),
#                 tableOutput("student_grades_table"),
#                 h4("Durchschnittsnote des Studenten"),
#                 textOutput("student_avg")
#        ),
#        
#        tabPanel("Exam",
#                 h3("Alle Noten eines Exams"),
#                 tableOutput("exam_grades_table"),
#                 h4("Durchschnittsnote des Exams"),
#                 textOutput("exam_avg"),
#                 plotOutput("exam_grades_plot")
#
#        ),
#        
#        tabPanel("Statistik",
#                 h3("Durchschnittsnoten aller Studenten"),
#                 tableOutput("all_gpa_table"),
#                 
#                 h4("Median der Durchschnittsnoten"),
#                 textOutput("median_gpa"),
#                 
#                 h4("Standardabweichung der Durchschnittsnoten"),
#                 textOutput("sd_gpa"),
#                 h4("Durchschnittsnoten pro Semester und Studiengang"),
#                 tableOutput("gpa_semester_program"),
#                 h4("Verteilung der Durchschnittsnoten"),
#                 plotOutput("all_gpa_plot")
#
#        )
#      )
#    )
#  )
#)
