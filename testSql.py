import mysql as sql
import mysql.connector as mysql

mydb = mysql.connect(
  host="localhost",
  user="root",
  password="",
  database = "provasimone"
)

#print(mydb)

cursor = mydb.cursor()

## getting all the tables which are present in 'datacamp' database
cursor.execute("SHOW TABLES")

tables = cursor.fetchall() ## it returns list of tables present in the database

## showing all the tables one by one
'''for table in tables:
    print(table)'''

query = "SELECT nome_citta FROM citta where cittaID = 0"

cursor.execute(query)

## fetching all records from the 'cursor' object
records = cursor.fetchall()

## Showing the data
for record in records:
    print('pippo')
    print(type(record[0]))