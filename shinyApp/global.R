library(shiny)
library(DBI)
library(RPostgres)
library(ggplot2)

# ===========================
# Datenbankverbindung
# ===========================
con <- dbConnect(
  RPostgres::Postgres(),
  dbname = "businessanalytics_new",
  host = "localhost",
  port = 5432,
  user = "johannesschmid"
)
