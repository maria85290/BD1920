#!/bin/python3
from datetime import datetime, timedelta
from calendar import monthrange

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
    return random.randint(1, monthrange(year, month)[1])


consultas = {}


def encontrar_primeira_data_hora_disponivel(year, month, day, hour, minute):
    global consultas

    data_hora = datetime(year, month, day, hour, minute)

    id_medico = 1
    while id_medico in consultas and data_hora.strftime('%Y-%m-%dT%H:%M') in consultas[id_medico]:
        if id_medico < len(consultas):
            id_medico += 1
        else:
            data_hora += timedelta(minutes=15)

            if data_hora.hour >= 18:
                # Depois da hora do fecho, voltamos a abrir às 9:00 do dia seguinte
                data_hora = data_hora.replace(hour=9, minute=0)
                data_hora += timedelta(days=1)

            id_medico = 1
    
    data_hora = data_hora.strftime('%Y-%m-%dT%H:%M')
    if data_hora not in consultas:
        consultas[data_hora] = [medico]
    else:
        consultas[data_hora].append(medico)

    return data_hora


if __name__ == "__main__":
    # DONE: Elaminar a possibilidade de médicos poderem dar diferentes consultas à mesma hora
    # TODO: Procedimento para iluminar todos os testes clínicos cuja data já passou, mas não foram realizados

    # UPDATE TesteClinico SET realizado=1 WHERE id_testeclinico=%d;
    random.seed(0)

    atletas = read_file('atletas.txt')
    medicos = read_file('medicos.txt')
    modalidades = read_file('modalidades.txt')
    tipos_testes = read_file('testes.txt')
    freguesias = read_file('freguesias_braga.txt')

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

        print(f"INSERT INTO Prova (data_hora, duração, id_modalidade) VALUES ('{data_hora}', {duracao}, {id_modalidade});")

    i = 1
    for _ in range(random.randint(1, 60)): # Selecionar o nº de testes que vamos inserir
        id_atelta_que_realizou = random.randint(1, len(atletas))

        for _ in range(random.randint(1, 3)):
            year = random.randint(2019, 2021)
            month = random.randint(1, 12)
            day = gerar_dia(year, month)
            hour = random.randint(9, 17)
            minute = random.choice([0, 15, 30, 45])
            data_hora = encontrar_primeira_data_hora_disponivel(year, month, day, hour, minute)

            # nome = random.choice(tipos_testes) # ??
            nome = 'Análises'
            realizado = random.randint(0, 1) if datetime.fromisoformat(data_hora) < datetime.now() else 0
            preco = random.randint(5, 15) # 5-15 €

            id_medico_que_realizou = random.randint(1, len(medicos))

            print(f"INSERT INTO TesteClinico (nome, realizado, preço, data_hora, id_atleta, id_profissional) VALUES ('{nome}', {realizado}, {preco}, '{data_hora}', {id_atelta_que_realizou}, {id_medico_que_realizou});")

            i += 1

    for j in range(3):
        year = 2020
        month = 1
        day = 3 + j
        hour = random.randint(9, 17)
        minute = random.choice([0, 15, 30, 45])
        data_hora = encontrar_primeira_data_hora_disponivel(year, month, day, hour, minute)

        # nome = random.choice(tipos_testes) # ??
        nome = 'Análises'
        realizado = random.randint(0, 1) if datetime.fromisoformat(data_hora) < datetime.now() else 0
        preco = random.randint(5, 15) # 5-15 €

        id_medico_que_realizou = random.randint(1, len(medicos))
        id_atelta_que_realizou = random.randint(1, len(atletas))

        print(f"INSERT INTO TesteClinico (nome, realizado, preço, data_hora, id_atleta, id_profissional) VALUES ('{nome}', {realizado}, {preco}, '{data_hora}', {id_atelta_que_realizou}, {id_medico_que_realizou});")

        i += 1
