import pyodbc

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=STEVE;"
    "Database=ToDoList;"
    "Trusted_Connection=yes;"
)

