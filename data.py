import pyodbc

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=STEVE;"
    "Database=QLNhaTro;"
    "Trusted_Connection=yes;"
)

