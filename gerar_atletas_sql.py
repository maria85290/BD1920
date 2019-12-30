#!/bin/python3
import sys
import os
import random
import numpy.random


def read_file(filename):
    if not os.path.exists(filename):
        exit(-1)

    with open(filename) as file:
        return [x.strip() for x in file.readlines() if x.strip() != ""]


def gerar_dia(year, month):
    dayEdge = 31

    if month % 2 == 1:
        dayEdge = 30

    if month == 2:
            dayEdge = 28
    
    return random.randint(1, dayEdge)

if __name__ == "__main__":
    random.seed(0)

    atletas = read_file('atletas.txt')
    medicos = read_file('medicos.txt')
    modalidades = read_file('modalidades.txt')
    tipos_testes = read_file('testes.txt')
    freguesias = read_file('freguesias_braga.txt')
    provas = read_file('provas.txt')

    primeiros_nomes_genero = {}
    for x in read_file('primeiros_nomes_genero.txt'):
        x = x.strip().split()
        primeiros_nomes_genero[x[0]] = x[1]

    # Selecionar o número de profissionais e de atletas que vamos efetivamente meter na DB
    medicos = [x for x in medicos if random.randint(1, 10) == 1] # Inserir apenas 1/6 dos profissionais
    atletas = [x for x in atletas if random.randint(1, 3) == 1] # Inserir apenas 1/3 dos atletas

    for modalidade in modalidades:
        print(f"INSERT INTO Modalidade (nome) VALUES ('{modalidade}');")
    
    for medico in medicos:
        print(f"INSERT INTO Profissional (nome) VALUES ('{medico}');")

    # Cada atleta tem:
    ## id
    ## sexo
    ## nome
    ## peso
    ## altura
    ## morada
    ## date of birth
    ## modalidade que pratica
    for nome_atleta in atletas:
        sexo = primeiros_nomes_genero[nome_atleta.split()[0]]
        peso = round(numpy.random.normal(100, 20)) # mu=100Kg, sigma=20
        altura = round(numpy.random.normal(200, 20)) # mu=200cm, sigma=20
        morada = '{}, Braga'.format(random.choice(freguesias))

        year = random.randint(1975, 1995)
        month = random.randint(1, 12)
        day = gerar_dia(year, month)
        dob = '{}-{}-{}'.format(year, month, day)

        modalidade = random.randint(1, len(modalidades))

        print(f"INSERT INTO Atleta (sexo, nome, peso, altura, morada, DOB, id_modalidade)",
              f"VALUES ('{sexo}', '{nome_atleta}', '{peso}', '{altura}', '{morada}', '{dob}', {modalidade});")

    # Cada prova tem:
    ## id
    ## data_hora
    ## duração
    ## nome
    ## id_modalidade
    for id_modalidade in range(1, len(modalidades) + 1):
        year = random.randint(2020, 2021)
        month = random.randint(1, 12)
        day = gerar_dia(year, month)
        hour = random.randint(9, 20)
        minute = random.randint(0, 59)
        data_hora = '{}-{}-{}T{}:{}'.format(year, month, day, hour, minute)

        duracao = random.randint(1, 2048)
        nome = modalidades[id_modalidade - 1]

        print(f"INSERT INTO Prova (data_hora, duração, nome, id_modalidade) VALUES ('{data_hora}', {duracao}, '{nome}', {id_modalidade});")


    i = 1
    for _ in range(random.randint(1, 60)): # Selecionar o nº de testes que vamos inserir
        year = random.randint(2020, 2021)
        month = random.randint(1, 12)
        day = gerar_dia(year, month)
        hour = random.randint(9, 20)
        minute = random.randint(0, 59)
        data_hora = '{}-{}-{}T{}:{}'.format(year, month, day, hour, minute)

        nome = random.choice(tipos_testes) # ??
        realizado = random.randint(0, 1)
        preco = random.randint(5, 15) # 5-15 €
        duracao = random.randint(5, 30) # 5-30 mins

        id_medico_que_realizou = random.randint(1, len(medicos))
        id_atelta_que_realizou = random.randint(1, len(atletas))

        print(f"INSERT INTO TestesClinicos (nome, realizado, preço, duração, data_hora) VALUES ('{nome}', {realizado}, {preco}, {duracao}, '{data_hora}');")
        print(f"INSERT INTO Teste_Profissional (id_teste_clinico, id_profissional) VALUES ({i}, {id_medico_que_realizou});")
        print(f"INSERT INTO Atleta_Testes_Clinicos (id_teste_clinico, id_atleta) VALUES ({i}, {id_atelta_que_realizou});")

        i += 1
    