import mysql.connector as sql

mydb = sql.connect(
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
    print(record[0])

# Connessione al database 
mydb = sql.connect(
        host="5.135.165.96",
        user="chatbot",
        password="kaffeehouse",
        database = "chatbot"
        )
cursor = mydb.cursor()

nome_allergene="'%"+"pippo"+"%'"
query = 'select name, ingredients, energy_kcal_value, allergens from mulino_bianco where allergens NOT LIKE '+nome_allergene
query2 = 'select name, ingredients, energy_kcal_value, allergens from mulino_bianco'
cursor.execute(query)

allergeni_result = cursor.fetchall()
cursor.execute(query2)
test = cursor.fetchall()
print()
print()

if len(test) == len(allergeni_result):
  print("Tutti i prodotti della mulino bianco non presentano l'alimento a cui sei allergico")
else:
  print("Ho filtrato il risultato")
result = list(filter(lambda x: True if 'olio di girasole' in x[1] else False, allergeni_result)) 
print(len(result))
print(type(result[1]))
result2 = list(filter(lambda x: x[0]== 'abbracci', result)) 
print(result2)
