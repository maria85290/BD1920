import mysql.connector
from pymongo import MongoClient
from datetime import date
from datetime import datetime
from getpass import getpass

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = getpass("MySQL password: "),
    database = "TestesClinicos",
    auth_plugin = "mysql_native_password"
)

print("Connecting to MySQL database...")
cursor = mydb.cursor()

print("Querying MySQL TestesClinicos...")
query_provas = open("provas.sql").read()
query_testes = open("testes.sql").read()

cursor.execute(query_testes)
results_testes = cursor.fetchall()

cursor.execute(query_provas)
results_provas = cursor.fetchall()

print("Converting entries to documents..")
converted_results_provas = list(map(lambda entry: {"data_hora": entry[0], "duração": entry[1], "nome_modalidade": entry[2]}, results_provas))
converted_results_testes = list(map(lambda entry: {"tipo": entry[0], "realizado": bool(entry[1]), "preço": entry[2], "data_hora": entry[3], "atleta": {"nome": entry[4], "sexo": entry[5], "modalidade": entry[6], "peso": entry[7], "morada": entry[8], "DOB": datetime.combine(entry[9], datetime.min.time())}, "profissional" : {"nome": entry[10]}}, results_testes))

print("Connecting to MongoDB...")
mongo_client = MongoClient('localhost', 27017)

if "TestesClinicos" in mongo_client.list_database_names():
    print("TestesClinicos already exists.")
    answer = input("You wish to drop it? 'y' to Yes, anything else to No.\n")
    if answer.lower() == 'y':
        mongo_client.drop_database("TestesClinicos")

        testesClinicos = mongo_client["TestesClinicos"]
        prova = testesClinicos["Prova"]
        testeClinico = testesClinicos["TesteClinico"]

        print("Inserting documents...")
        for document in converted_results_provas:
            prova.insert_one(document)

        for document in converted_results_testes:
            testeClinico.insert_one(document)

        print("Done!")

    else:
        print("Cancelled.")