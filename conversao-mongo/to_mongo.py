#!/bin/python3

import mysql.connector
from pymongo import MongoClient
from datetime import date
from datetime import datetime
from getpass import getpass
import sys

if __name__ == "__main__":
    print("Connecting to MySQL database...")

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = getpass("MySQL password: "),
        database = "TestesClinicos",
        auth_plugin = "mysql_native_password"
    )

    cursor = mydb.cursor()

    print("Querying MySQL TestesClinicos...")

    query_prova = "SELECT p.data_hora, p.duração, m.nome FROM Prova p \
                   INNER JOIN Modalidade m ON p.id_modalidade = m.id_modalidade;"
                   
    query_teste = "SELECT tc.nome, tc.realizado, tc.preço, tc.data_hora, atl.nome AS 'nome_atleta', atl.sexo AS 'sexo_atleta', \
                          m.nome AS 'modalidade_atleta', atl.peso AS 'peso_atleta', atl.morada as 'morada_atleta', \
                          atl.DOB as 'DOB_atleta', prof.nome as 'nome_professional' FROM TesteClinico tc \
                   INNER JOIN Atleta atl ON atl.id_atleta = tc.id_atleta \
                   INNER JOIN Profissional prof ON prof.id_profissional = tc.id_profissional \
                   INNER JOIN Modalidade m ON atl.id_modalidade = m.id_modalidade;"

    cursor.execute(query_teste)
    results_teste = cursor.fetchall()

    cursor.execute(query_prova)
    results_prova = cursor.fetchall()

    print("Converting entries to documents...")

    converted_results_prova = list(map(lambda entry: {"data_hora": entry[0], "duração": entry[1], "modalidade": entry[2]}, results_prova))
    converted_results_teste = list(map(lambda entry: {"tipo": entry[0], "realizado": bool(entry[1]), "preço": entry[2], "data_hora": entry[3], "atleta": {"nome": entry[4], "sexo": entry[5], "modalidade": entry[6], "peso": entry[7], "morada": entry[8], "DOB": datetime.combine(entry[9], datetime.min.time())}, "profissional" : {"nome": entry[10]}}, results_teste))

    print("Connecting to MongoDB...")

    mongo_client = MongoClient('localhost', 27017)

    if "TestesClinicos" in mongo_client.list_database_names():
        print("TestesClinicos already exists.")
        answer = input("You wish to drop it? 'y' to Yes, anything else to No.\n")

        if answer.lower() == 'y':
            mongo_client.drop_database("TestesClinicos")

        else:
            print("Cancelled.")
            sys.exit()

    testesClinicos = mongo_client["TestesClinicos"]
    prova = testesClinicos["Prova"]
    testeClinico = testesClinicos["TesteClinico"]

    print("Inserting documents...")
    
    for document in converted_results_prova:
        prova.insert_one(document)

    for document in converted_results_teste:
        testeClinico.insert_one(document)

    print("Done!")