library(shiny)
library(DBI)
library(RPostgres)
library(ggplot2)

# ===========================
# Datenbankverbindung
# ===========================
con <- dbConnect(
  RPostgres::Postgres(),
  dbname="examdb",#examdb
  user="postgres",
  password="12345",  # wie in db.py
  host="localhost",
  port="5432"
)
